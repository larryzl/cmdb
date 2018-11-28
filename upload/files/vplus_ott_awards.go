/**
* adv awards
* v3.8
* tansuotv.com
**/
package main

import (
	"bytes"
	"crypto/sha1"
	"crypto/x509"
	"encoding/hex"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"github.com/hyperledger/fabric/core/chaincode/shim"
	sc "github.com/hyperledger/fabric/protos/peer"
	"sort"
	"strconv"
	"strings"
	"time"
)

type SmartContract struct {
}

//定义用户账户结构
type DeviceAccount struct {
	DeviceID     string  `json:"deviceid"`
	JoinTime     string  `json:"jointime"`
	Brand        string  `json:"brand"`
	Level        string  `json:"level"`
	Balance      float64 `json:"balance"`
	Status       int     `json:"status"`
	Organization string  `json:"organization"`
	Channel      string  `json:"channel"`
	LastAction   string  `json:"lastaction"`
	TotalaIssue  float64 `json:"totalissue"`
}

//定义奖励行为数据结构
/*type DetailsItem struct {
	DetailType   string `json:"detailtype"`
	AlbumID      string `json:"albumid"`
	MoviesID     string `json:"moviesid"`
	PlayTime     string `json:"playtime"`
	OrderID      string `json:"orderid"`
	MaterialID   string `json:"materialid"`
	InteractType string `json:"interacttype"`
	TaskID       string `json:"taskid"`
	TaskName     string `json:"taskname"`
}*/

/*
//定义发币用户集
type IssueAccount struct{
        ID int `json:"id"`
        JoinTime string `json:"jointime"`
        Level string `json:"level"`
        Balance float64 `json:"balance"`
        ToalaIssue float64 `json:"totalissue"`
        Status int `json:"status"`
}
*/

//定义账户明细结构
type AccountDetails struct {
	ID       string  `json:"id"`       //应用中的交易ID
	Time     string  `json:"time"`     //发生时间
	DeviceID string  `json:"deviceid"` //输入方钱包地址
	Price    float64 `json:"price"`    //发生金额
	Type     int     `json:"type"`     //交易类型 2奖励 1消费 3转账
	Action   string  `json:"action"`   //交易动作 比如看视频奖励等
	From     string  `json:"from"`     //输出方钱包地址
	TxID     string  `json:"txid"`     //区块链交易ID
	//Detail   DetailsItem `json:"detailitem"`
	Detail    []string `json:"detail"` //空字段，保留，原为动作明细hash
	DetailStr []string `json:"detailstr"`
	Balance   float64  `json:"balance"` //当前钱包余额
	IsQuery   int      `json:"isquery"` //是否查询结果(不写数据库)
}

//定义总终端数
type TotalAccount struct {
	Total int `json:"total"`
}
type TotalDetails struct {
	Total int `json"total"`
}

//初始化，定义发行账户
func (s *SmartContract) Init(APIstub shim.ChaincodeStubInterface) sc.Response {
	//V+总池
	acountspool := DeviceAccount{DeviceID: "TS_BLOCKCHAIN_POOL", JoinTime: "", Brand: "V+", Level: "9", Balance: 10000000000, Status: 1, Organization: "V+", Channel: "", LastAction: "", TotalaIssue: 10000000000}
	acountspoolAsBytes, _ := json.Marshal(acountspool)
	APIstub.PutState("ACCOUNT_TS_BLOCKCHAIN_POOL", acountspoolAsBytes)
	//V+用户奖励池
	accounts := DeviceAccount{DeviceID: "TS_BLOCKCHAIN", JoinTime: "", Brand: "V+", Level: "8", Balance: 0, Status: 1, Organization: "V+", Channel: "", LastAction: "", TotalaIssue: 0}
	acountsAsBytes, _ := json.Marshal(accounts)
	APIstub.PutState("ACCOUNT_TS_BLOCKCHAIN", acountsAsBytes)
	//总池向奖励池进行转账
	acountspool.Balance = acountspool.Balance - 3000000000
	acountspoolAsBytes, _ = json.Marshal(acountspool)
	APIstub.PutState("ACCOUNT_TS_BLOCKCHAIN_POOL", acountspoolAsBytes)
	accounts.Balance = accounts.Balance + 3000000000
	accounts.TotalaIssue = accounts.TotalaIssue + 3000000000
	acountsAsBytes, _ = json.Marshal(accounts)
	APIstub.PutState("ACCOUNT_TS_BLOCKCHAIN", acountsAsBytes)
	//detail_item := DetailsItem{DetailType: "transfer", AlbumID: "", MoviesID: "", PlayTime: "", OrderID: "", MaterialID: "", InteractType: "", TaskID: "", TaskName: ""}
	detail := AccountDetails{
		ID:       "0",
		Time:     "2018-05-25 00:00:00",
		DeviceID: "TS_BLOCKCHAIN",
		OrderID:  "",
		Price:    3000000000,
		Type:     9,
		Action:   "transfer",
		From:     "TS_BLOCKCHAIN_POOL",
		To:       "TS_BLOCKCHAIN",
		Detail:   "",
		IsQuery:  0,
	}
	detailAsByes, _ := json.Marshal(detail)
	APIstub.PutState("DETAIL_0", detailAsByes)
	/*
		tsaccountAsBytes, _ := APIstub.GetState("ACCOUNT_TS_BLOCKCHAIN")
		tsaccount_info := DeviceAccount{}
		json.Unmarshal(tsaccountAsBytes, &tsaccount_info)
		tsaccount_info.TotalaIssue = 3000000000
		tsaccountAsBytes, _ = json.Marshal(tsaccount_info)
		APIstub.PutState("ACCOUNT_TS_BLOCKCHAIN", tsaccountAsBytes)

		i: = 1;
		  //获得已发放余额
		  tsaccountAsBytes,_ := APIstub.GetState("ACCOUNT_TS_BLOCKCHAIN")
		  tsaccount_info := DeviceAccount{}
		  json.Unmarshal(tsaccountAsBytes,&tsaccount_info)
		  total_accounts := 10000;
		  total_accounts_folat := strconv.ParseFloat(total_accounts, 64)
		  every_accrount_balance := tsaccount_info.balance / total_accounts_folat
		  for i <=10000{
		          account :=  IssueAccount{
		                  ID : i,
		                  JoinTime : "",
		                  Level : "9",
		                  Balance : every_accrount_balance,
		                  Status : 1,
		          }
		          key :=  "ISSUE_ACCOUNT:"+strconv.Itoa(account.ID)
		          accountJsonBytes, err := json.Marshal(account)//Json序列号
		          stub.PutState(key,accountJsonBytes)
		          i = i + 1
		  }
		  tsaccount_info.Balance = 0
		  tsaccountAsBytes,_ = json.Marshal(tsaccount_info)
		  APIstub.PutState("ACCOUNT_TS_BLOCKCHAIN",tsaccountAsBytes)*/

	/*accounts := []DeviceAccount{
		DeviceAccount{DeviceID: "TS_BLOCKCHAIN", JoinTime: "", Brand: "TanSuo", Level: "9", Balance: 3000000000, Status: 1, Organization: "TanSuo", Channel: "", LastAction: "", TotalaIssue: 3000000000},
	}
	//length := TotalAccount{Total:len(accounts)}
	//lengthAsBytes,_ := json.Marshal(length)
	//APIstub.PutState("TOTALACCOUNT", lengthAsBytes)
	i := 0
	for i < len(accounts) {
		accountAsBytes, _ := json.Marshal(accounts[i])
		APIstub.PutState("ACCOUNT_"+accounts[i].DeviceID, accountAsBytes)
		i = i + 1
	}
	/*details_count := TotalDetails{Total:0}
	  totalAsBytes,_ := json.Marshal(details_count)
	  APIstub.PutState("TOTALDETAILS",totalAsBytes)*/
	return shim.Success(nil)
}
func (s *SmartContract) Invoke(APIstub shim.ChaincodeStubInterface) sc.Response {
	function, args := APIstub.GetFunctionAndParameters()
	if function == "AccountInfo" {
		//账户查询
		return s.AccountInfo(APIstub, args)
	} else if function == "InitAccount" {
		//初始化账户
		return s.InitAccount(APIstub, args)
	} else if function == "QueryDetailByID" {
		//查询某条交易记录
		return s.QueryDetailByID(APIstub, args)
	} else if function == "AccountInfoByUser" {
		//不通过证书查询用户账户
		return s.AccountInfoByUser(APIstub, args)
	} else if function == "UpdateTsAccount" {
		//更新探索账户
		return s.UpdateTsAccount(APIstub, args)
	} else if function == "RichQueryByDevice" {
		return s.RichQueryByDevice(APIstub, args)
	} else if function == "getDetailByList" {
		return s.getDetailByList(APIstub, args)
	} else if function == "RepostDeviceBatch" {
		return s.RepostDeviceBatch(APIstub, args)
	}

	return shim.Error("Invalid Smart Contract function name.")
}

func (s *SmartContract) QueryDetailByID(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {
	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}
	detailAsByes, _ := APIstub.GetState("DETAIL_" + args[0])
	if detailAsByes == nil {
		//fmt.Errorf(format, ...)
		return shim.Success(nil)
	}
	detail_info := AccountDetails{}
	json.Unmarshal(detailAsByes, &detail_info)
	if detail_info.Balance == 0 {
		deviceid := detail_info.DeviceID
		accountAsBytes, _ := APIstub.GetState("ACCOUNT_" + deviceid)
		account_info := DeviceAccount{}
		json.Unmarshal(accountAsBytes, &account_info)
		detail_info.Balance = account_info.Balance
		detailAsByes, _ = json.Marshal(detail_info)
	}
	return shim.Success(detailAsByes)
}

//批量查询交易
func (s *SmartContract) getDetailByList(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {
	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}
	list := strings.Split(args[0], ",")
	i := 0
	var buffer bytes.Buffer
	buffer.WriteString("[")

	bArrayMemberAlreadyWritten := false
	for i < len(list) {
		detailAsByes, _ := APIstub.GetState("DETAIL_" + list[i])
		if detailAsByes != nil {
			if bArrayMemberAlreadyWritten == true {
				buffer.WriteString(",")
			}
			buffer.WriteString(string(detailAsByes))
			bArrayMemberAlreadyWritten = true
		}
		i = i + 1
	}
	buffer.WriteString("]")
	return shim.Success(buffer.Bytes())
}

func (s *SmartContract) RepostDeviceBatch(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {
	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}
	list := strings.Split(args[0], "{||}")
	txID := APIstub.GetTxID()
	i := 0
	device_list := map[string]DeviceAccount{}
	detail_maps := map[string]int{}
	ts := time.Now().Unix()
	tssrt := strconv.FormatInt(ts, 10)
	for i < len(list) {
		var dat map[string]interface{}
		if err := json.Unmarshal([]byte(list[i]), &dat); err == nil {
			//检查交易是否存在
			new_detail := AccountDetails{}
			tx_ := []byte(list[i])
			json.Unmarshal(tx_, &new_detail)
			if _, detail_map_item := detail_maps[new_detail.ID]; !detail_map_item {
				check_detailAsByes, _ := APIstub.GetState("DETAIL_" + new_detail.ID)
				if check_detailAsByes != nil {
					detail_maps[new_detail.ID] = 1
				} else {
					detail_maps[new_detail.ID] = 0
				}
			} else {
				detail_maps[new_detail.ID] = 1
			}

			if detail_maps[new_detail.ID] == 1 {
				//已存在的交易
			} else {
				//不存在的交易
				//查找钱包信息
				account_info := DeviceAccount{}
				if _, account_item := device_list[new_detail.DeviceID]; !account_item {
					accountAsBytes, err := APIstub.GetState("ACCOUNT_" + new_detail.DeviceID)
					if err != nil {
						fmt.Errorf("GetAccount Error")
					}
					if accountAsBytes == nil {
						account := DeviceAccount{DeviceID: new_detail.DeviceID, JoinTime: tssrt, Brand: "V+", Level: "1", Balance: 0, Status: 1, Organization: "", Channel: "", LastAction: tssrt}
						accountAsBytes, _ = json.Marshal(account)
					}
					json.Unmarshal(accountAsBytes, &account_info)
					device_list[new_detail.DeviceID] = account_info
				} else {
					account_info = device_list[new_detail.DeviceID]
				}
				price := new_detail.Price
				//增加奖励金额
				account_info.Balance = account_info.Balance + price
				//更新账户信息
				accountAsBytes, _ := json.Marshal(account_info)
				APIstub.PutState("ACCOUNT_"+new_detail.DeviceID, accountAsBytes)
				device_list[new_detail.DeviceID] = account_info
				//固定奖励发送账户
				new_detail.From = "ACCOUNT_TS_BLOCKCHAIN"
				//设置交易时间
				new_detail.Time = tssrt
				//获取当前钱包余额
				new_detail.Balance = account_info.Balance
				//写入提案ID
				new_detail.TxID = txID

				//准备明细数据（hash）
				j := 0
				detail := (dat["detail"].([]interface{}))
				var tx_hash []string
				var detail_map map[string]interface{}
				for j < len(detail) {
					hash := ""
					detail_map = detail[j].(map[string]interface{})
					var keys []string
					for k := range detail_map {
						keys = append(keys, k)
					}
					sort.Strings(keys)
					key_i := 0
					for _, k := range keys {
						key_i = key_i + 1
						hash += k + "=" + detail_map[k].(string)
						if key_i < len(keys) {
							hash += "{||}"
						}
					}
					hash += "{||}" + txID
					sha1 := sha1.New()
					sha1.Write([]byte(hash))
					hash = hex.EncodeToString(sha1.Sum([]byte("")))
					tx_hash = append(tx_hash, hash)
					j = j + 1
				}
				//写入交易明细HASH
				new_detail.Detail = tx_hash
				//交易信息更新
				detailAsByes, _ := json.Marshal(new_detail)
				APIstub.PutState("DETAIL_"+new_detail.ID, detailAsByes)
				detail_maps[new_detail.ID] = 1
			}
		}
		i = i + 1
	}
	return shim.Success(nil)
}

func (s *SmartContract) RepostDeviceBatch2(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {
	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}
	list := strings.Split(args[0], "{||}")
	txID := APIstub.GetTxID()
	i := 0
	device_list := map[string]DeviceAccount{}
	detail_maps := map[string]int{}
	for i < len(list) {
		detail_ := []byte(list[i])

		new_detail := AccountDetails{}
		json.Unmarshal(detail_, &new_detail)
		if _, detail_map_item := detail_maps[new_detail.ID]; !detail_map_item {
			check_detailAsByes, _ := APIstub.GetState("DETAIL_" + new_detail.ID)
			if check_detailAsByes != nil {
				detail_maps[new_detail.ID] = 1
			} else {
				detail_maps[new_detail.ID] = 0
			}
		} else {
			detail_maps[new_detail.ID] = 0
		}

		if detail_maps[new_detail.ID] == 1 {
			//已存在的交易
		} else {
			//不存在的交易
			price := new_detail.Price
			account_info := DeviceAccount{}
			if _, account_item := device_list[new_detail.DeviceID]; !account_item {
				accountAsBytes, err := APIstub.GetState("ACCOUNT_" + new_detail.DeviceID)
				if err != nil {
					fmt.Errorf("GetAccount Error")
				}

				if accountAsBytes == nil {
					//创建账户
					ts := time.Now().Unix()
					tssrt := strconv.FormatInt(ts, 10)
					account := DeviceAccount{DeviceID: new_detail.DeviceID, JoinTime: tssrt, Brand: "V+", Level: "1", Balance: 0, Status: 1, Organization: "", Channel: "", LastAction: tssrt}
					accountAsBytes, _ = json.Marshal(account)
				}
				json.Unmarshal(accountAsBytes, &account_info)
				device_list[new_detail.DeviceID] = account_info
			} else {
				account_info = device_list[new_detail.DeviceID]
			}
			account_info.Balance = account_info.Balance + price
			accountAsBytes, _ := json.Marshal(account_info)
			APIstub.PutState("ACCOUNT_"+new_detail.DeviceID, accountAsBytes)
			device_list[new_detail.DeviceID] = account_info
			new_detail.From = "ACCOUNT_TS_BLOCKCHAIN"
			new_detail.Balance = account_info.Balance
			new_detail.TxID = txID
			detail := new_detail
			detailAsByes, _ := json.Marshal(detail)
			APIstub.PutState("DETAIL_"+new_detail.ID, detailAsByes)
			detail_maps[new_detail.ID] = 1
		}
		i = i + 1
	}
	return shim.Success(nil)
}

func (s *SmartContract) UpdateTsAccount(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {
	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}
	tsaccountAsBytes, _ := APIstub.GetState("ACCOUNT_TS_BLOCKCHAIN")
	tsaccount_info := DeviceAccount{}
	json.Unmarshal(tsaccountAsBytes, &tsaccount_info)
	reduce, err := strconv.ParseFloat(args[0], 64)
	if err != nil {
		return shim.Error("Incorrect number of arguments. Expecting 2")
	}
	new_balance := tsaccount_info.Balance - reduce
	tsaccount_info.Balance = new_balance
	tsaccountAsBytes, _ = json.Marshal(tsaccount_info)
	APIstub.PutState("ACCOUNT_TS_BLOCKCHAIN", tsaccountAsBytes)
	var buffer bytes.Buffer
	buffer.WriteString("{\"TotalIssue\":")
	buffer.WriteString("\"")
	buffer.WriteString(strconv.FormatFloat((tsaccount_info.TotalaIssue), 'E', -1, 64))
	buffer.WriteString("\"")
	buffer.WriteString(", \"Balance\":")
	buffer.WriteString("\"")
	buffer.WriteString(strconv.FormatFloat((tsaccount_info.Balance), 'E', -1, 64))
	buffer.WriteString("\"")
	buffer.WriteString("}")
	return shim.Success(buffer.Bytes())
}

func (s *SmartContract) InitAccount(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {
	if len(args) != 4 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}
	creatorByte, _ := APIstub.GetCreator()
	certStart := bytes.IndexAny(creatorByte, "-----BEGIN")
	if certStart == -1 {
		fmt.Errorf("No certificate found")
	}
	certText := creatorByte[certStart:]
	bl, _ := pem.Decode(certText)
	if bl == nil {
		fmt.Errorf("Could not decode the PEM structure")
	}
	cert, err := x509.ParseCertificate(bl.Bytes)
	if err != nil {
		fmt.Errorf("ParseCertificate failed")
	}
	uname := cert.Subject.CommonName
	//lengthAsBytes, _ := APIstub.GetState("TOTALACCOUNT")
	//length := TotalAccount{}
	//json.Unmarshal(lengthAsBytes,&length)
	//newlength := length.Total+1
	account := DeviceAccount{DeviceID: uname, JoinTime: args[0], Brand: args[1], Level: "1", Balance: 0, Status: 1, Organization: args[2], Channel: args[3], LastAction: args[0]}
	accountAsBytes, _ := json.Marshal(account)
	APIstub.PutState("ACCOUNT_"+account.DeviceID, accountAsBytes)
	//length.Total = newlength
	//lengthAsBytes,_ = json.Marshal(length)
	//APIstub.PutState("TOTALACCOUNT",lengthAsBytes)
	name_ := []byte(uname)
	return shim.Success(name_)
}

//通过证书获取该终端证书
func (s *SmartContract) AccountInfo(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {
	creatorByte, _ := APIstub.GetCreator()
	certStart := bytes.IndexAny(creatorByte, "-----BEGIN")
	if certStart == -1 {
		fmt.Errorf("No certificate found")
	}
	certText := creatorByte[certStart:]
	bl, _ := pem.Decode(certText)
	if bl == nil {
		fmt.Errorf("Could not decode the PEM structure")
	}
	cert, err := x509.ParseCertificate(bl.Bytes)
	if err != nil {
		fmt.Errorf("ParseCertificate failed")
	}
	uname := cert.Subject.CommonName
	postAsBytes, _ := APIstub.GetState("ACCOUNT_" + uname)
	return shim.Success(postAsBytes)
}

//管理员身份获取指定终端账户信息
func (s *SmartContract) AccountInfoByUser(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {
	var deviceid = args[0]

	/*
	   creatorByte, _ := APIstub.GetCreator()
	   certStart := bytes.IndexAny(creatorByte, "-----BEGIN")
	   if certStart == -1 {
	           fmt.Errorf("No certificate found")
	   }
	   if len(args) != 1 || deviceid == ""   {
	           return shim.Error("Incorrect number of arguments. Expecting 1")
	   }
	   certText := creatorByte[certStart:]
	   bl, _ := pem.Decode(certText)
	   if bl == nil {
	           fmt.Errorf("Could not decode the PEM structure")
	   }
	   cert, err := x509.ParseCertificate(bl.Bytes)
	   if err != nil {
	           fmt.Errorf("ParseCertificate failed")
	   }
	   uname := cert.Subject.CommonName
	*/

	//判断是否为管理员证书
	postAsBytes, _ := APIstub.GetState("ACCOUNT_" + deviceid)
	return shim.Success(postAsBytes)
}

func getListResult(resultsIterator shim.StateQueryIteratorInterface) ([]byte, error) {

	defer resultsIterator.Close()
	// buffer is a JSON array containing QueryRecords
	var buffer bytes.Buffer
	buffer.WriteString("[")

	bArrayMemberAlreadyWritten := false
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}
		// Add a comma before array members, suppress it for the first array member
		if bArrayMemberAlreadyWritten == true {
			buffer.WriteString(",")
		}
		buffer.WriteString("{\"Key\":")
		buffer.WriteString("\"")
		buffer.WriteString(queryResponse.Key)
		buffer.WriteString("\"")

		buffer.WriteString(", \"Record\":")
		// Record is a JSON object, so we write as-is
		buffer.WriteString(string(queryResponse.Value))
		buffer.WriteString("}")
		bArrayMemberAlreadyWritten = true
	}
	buffer.WriteString("]")
	fmt.Printf("queryResult:\n%s\n", buffer.String())
	return buffer.Bytes(), nil
}

func (t *SmartContract) RichQueryByDevice(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {
	name := args[0]
	queryString := fmt.Sprintf("{\"selector\":{\"DeviceID\":\"%s\"}}", name)
	resultsIterator, err := APIstub.GetQueryResult(queryString) //必须是CouchDB才行
	if err != nil {
		return shim.Error("Rich query failed")
	}
	students, err := getListResult(resultsIterator)
	if err != nil {
		return shim.Error("Rich query failed")
	}
	return shim.Success(students)
}

func main() {
	err := shim.Start(new(SmartContract))
	if err != nil {
		fmt.Printf("Error starting Simple chaincode: %s", err)
	}
}
