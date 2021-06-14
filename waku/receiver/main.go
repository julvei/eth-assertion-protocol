package main

import (
	"chat2/pb"
	"context"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	mrand "math/rand"
	"net"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/ethereum/go-ethereum/crypto"
	logging "github.com/ipfs/go-log"
	"github.com/libp2p/go-libp2p-core/peer"
	"github.com/status-im/go-waku/waku/v2/node"
	"github.com/status-im/go-waku/waku/v2/protocol/store"
)

//var DefaultContentTopic string = "dingpu"
var DefaultContentTopic string = "udtraei"

func main() {
	mrand.Seed(time.Now().UTC().UnixNano())

	nickFlag := flag.String("nick", "Validator", "nickname to use in chat. will be generated if empty")
	nodeKeyFlag := flag.String("nodekey", "", "private key for this node. will be generated if empty")
	staticNodeFlag := flag.String("staticnode", "/ip4/47.242.210.73/tcp/30303/p2p/16Uiu2HAmSyrYVycqBCWcHyNVQS6zYQcdQbwyov1CDijboVRsQS37", "connects to a node. will get a random node from fleets.status.im if empty")
	storeNodeFlag := flag.String("storenode", "/ip4/47.242.210.73/tcp/30303/p2p/16Uiu2HAmSyrYVycqBCWcHyNVQS6zYQcdQbwyov1CDijboVRsQS37", "connects to a store node to retrieve messages. will get a random node from fleets.status.im if empty")
	//staticNodeFlag := flag.String("staticnode", "/ip4/134.209.139.210/tcp/30303/p2p/16Uiu2HAmPLe7Mzm8TsYUubgCAW1aJoeFScxrLj8ppHFivPo97bUZ", "connects to a node. will get a random node from fleets.status.im if empty")
	//storeNodeFlag := flag.String("storenode", "/ip4/134.209.139.210/tcp/30303/p2p/16Uiu2HAmPLe7Mzm8TsYUubgCAW1aJoeFScxrLj8ppHFivPo97bUZ", "connects to a store node to retrieve messages. will get a random node from fleets.status.im if empty")
	//staticNodeFlag := flag.String("staticnode", "/ip4/104.154.239.128/tcp/30303/p2p/16Uiu2HAmJb2e28qLXxT5kZxVUUoJt72EMzNGXB47Rxx5hw3q4YjS", "connects to a node. will get a random node from fleets.status.im if empty")
	//storeNodeFlag := flag.String("storenode", "/ip4/104.154.239.128/tcp/30303/p2p/16Uiu2HAmJb2e28qLXxT5kZxVUUoJt72EMzNGXB47Rxx5hw3q4YjS", "connects to a store node to retrieve messages. will get a random node from fleets.status.im if empty")
	//staticNodeFlag := flag.String("staticnode", "", "connects to a node. will get a random node from fleets.status.im if empty")
	//storeNodeFlag := flag.String("storenode", "", "connects to a store node to retrieve messages. will get a random node from fleets.status.im if empty")
	port := flag.Int("port", 0, "port. Will be random if 0")

	flag.Parse()

	hostAddr, _ := net.ResolveTCPAddr("tcp", fmt.Sprintf("0.0.0.0:%d", *port))

	// use the nickname from the cli flag, or a default if blank
	nodekey := *nodeKeyFlag
	if len(nodekey) == 0 {
		var err error
		nodekey, err = randomHex(32)
		if err != nil {
			fmt.Println("Could not generate random key")
			return
		}
	}
	prvKey, err := crypto.HexToECDSA(nodekey)

	ctx := context.Background()
	wakuNode, err := node.New(ctx,
		node.WithPrivateKey(prvKey),
		node.WithHostAddress([]net.Addr{hostAddr}),
		node.WithWakuRelay(),
		node.WithWakuStore(false),
	)
	if err != nil {
		fmt.Print(err)
		return
	}

	// use the nickname from the cli flag, or a default if blank
	nick := *nickFlag
	if len(nick) == 0 {
		nick = defaultNick(wakuNode.Host().ID())
	}

	// join the chat
	chat, err := NewChat(wakuNode, wakuNode.Host().ID(), nick)
	if err != nil {
		panic(err)
	}

	// Display panic level to reduce log noise
	lvl, err := logging.LevelFromString("panic")
	if err != nil {
		panic(err)
	}
	logging.SetAllLoggers(lvl)

	// Connect to a static node or use random node from fleets.status.im
	go func() {
		time.Sleep(200 * time.Millisecond)

		staticnode := *staticNodeFlag
		storenode := *storeNodeFlag

		var fleetData []byte
		if len(staticnode) == 0 || len(storenode) == 0 {
			fleetData = getFleetData()
		}

		if len(staticnode) == 0 {
			displayMessage("No static peers configured. Choosing one at random from test fleet...")
			staticnode = getRandomFleetNode(fleetData)
		}

		err = wakuNode.DialPeer(staticnode)
		if err != nil {
			displayMessage("Could not connect to peer: " + err.Error())
			return
		} /* else {
			displayMessage("Connected to peer: " + staticnode)

		}*/

		if len(storenode) == 0 {
			displayMessage("No store node configured. Choosing one at random from test fleet...")
			storenode = getRandomFleetNode(fleetData)
		}

		storeNodeId, err := wakuNode.AddStorePeer(storenode)
		if err != nil {
			displayMessage("Could not connect to storenode: " + err.Error())
			return
		} /* else {
			displayMessage("Connected to storenode: " + storenode)
		} */

		time.Sleep(300 * time.Millisecond)
		//displayMessage("Querying historic messages")

		tCtx, _ := context.WithTimeout(ctx, 1*time.Second)
		wakuNode.Query(tCtx, []string{DefaultContentTopic}, 0, 0,
			store.WithAutomaticRequestId(),
			store.WithPeer(*storeNodeId),
			store.WithPaging(true, 0))

		if err != nil {
			displayMessage("Could not query storenode: " + err.Error())
		} /*else {
			chat.displayMessages(response.Messages)
		}*/
	}()

	var wg sync.WaitGroup
	wg.Add(1)
	go handleEvents(chat, &wg)
	wg.Wait()
}

/****************************** UI FUNCTIONS ******************************/

// Run starts the chat event loop in the background, then starts
// the event loop for the text UI.
/*
func Run(chat *Chat) {
	//displayMessage("Welcome")

	go handleEvents(chat)

	return
}
*/

// displayChatMessage writes a ChatMessage from the room to the message window,
// with the sender's nick.
func displayChatMessage(cm *pb.Chat2Message) {
	t := time.Unix(int64(cm.Timestamp), 0)
	prompt := fmt.Sprintf("<%s> %s:", t.Format("Jan 02, 15:04"), cm.Nick)
	fmt.Printf("%s %s\n", prompt, cm.Payload)
}

// displayMessage writes message to output
func displayMessage(msg string) {
	fmt.Println(msg)
}

// handleEvents runs an event loop that sends user input to the chat room
// and displays messages received from the chat room. It also periodically
// refreshes the list of peers in the UI.
func handleEvents(chat *Chat, wg *sync.WaitGroup) {
	for {
		select {
		/*
			case input := <-ui.inputCh:
				err := ui.chat.Publish(input)
				if err != nil {
					printErr("publish error: %s", err)
				}
		*/
		case m := <-chat.Messages:
			// when we receive a message from the chat room, print it to the message window
			fmt.Printf("%s\n", m.Payload)
			wg.Done()
		}
	}
}

/****************************** OLD FUNCTIONS ******************************/
// Generates a random hex string with a length of n
func randomHex(n int) (string, error) {
	bytes := make([]byte, n)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return hex.EncodeToString(bytes), nil
}

// printErr is like fmt.Printf, but writes to stderr.
func printErr(m string, args ...interface{}) {
	fmt.Fprintf(os.Stderr, m, args...)
}

// defaultNick generates a nickname based on the $USER environment variable and
// the last 8 chars of a peer ID.
func defaultNick(p peer.ID) string {
	return fmt.Sprintf("%s-%s", os.Getenv("USER"), shortID(p))
}

// shortID returns the last 8 chars of a base58-encoded peer id.
func shortID(p peer.ID) string {
	pretty := p.Pretty()
	return pretty[len(pretty)-8:]
}

func getFleetData() []byte {
	url := "https://fleets.status.im"
	httpClient := http.Client{
		Timeout: time.Second * 2,
	}

	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		log.Fatal(err)
	}

	res, getErr := httpClient.Do(req)
	if getErr != nil {
		log.Fatal(getErr)
	}

	if res.Body != nil {
		defer res.Body.Close()
	}

	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		log.Fatal(readErr)
	}

	return body
}

func getRandomFleetNode(data []byte) string {
	var result map[string]interface{}
	json.Unmarshal(data, &result)

	fleets := result["fleets"].(map[string]interface{})
	wakuv2Test := fleets["wakuv2.test"].(map[string]interface{})
	waku := wakuv2Test["waku"].(map[string]interface{})

	var wakunodes []string
	for v := range waku {
		wakunodes = append(wakunodes, v)
		break
	}

	randKey := wakunodes[mrand.Intn(len(wakunodes))]

	return waku[randKey].(string)
}
