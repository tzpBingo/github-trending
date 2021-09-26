package main

import (
	"encoding/base64"
	"io/ioutil"
	"os"
	"strings"
)

func main() {
	file, err := os.Open("C:/Users/i4/Desktop/fping-msys2.0/FAST_IPS.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()
	content, err := ioutil.ReadAll(file)
	ipstr := string(content)
	json := `{"v":"2","ps":"{ip}","add":"{ip}","port":443,"type":"","id":"63235d2c-e6ca-4d03-a6f7-7765733c307e","aid":2,"net":"ws","path":"/16e704ab/","host":"aws-sg.7465868.workers.dev","tls":"tls"}`
	ips := strings.Split(ipstr, "\n")
	vmess := ""
	for _, ip := range ips {
		v := strings.Replace(json, "{ip}", strings.ReplaceAll(ip, "\r", ""), -1)
		encoded := base64.StdEncoding.EncodeToString([]byte(v))
		encoded = "vmess://" + strings.ReplaceAll(encoded, "\n", "")
		vmess = vmess + encoded + "\n"
	}
	vvv := []byte(base64.StdEncoding.EncodeToString([]byte(vmess)))
	errwirte := ioutil.WriteFile("C:/Users/i4/Desktop/fping-msys2.0/VMESS.txt", vvv, 0644)
	if errwirte != nil {
		panic(errwirte)
	}
}
