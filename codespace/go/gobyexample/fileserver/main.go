package main

import (
	"fmt"
	"net/http"
)

func main() {

	http.Handle("/ucd/", http.StripPrefix("/ucd/", http.FileServer(http.Dir("./"))))

	err := http.ListenAndServe(":11080", nil)
	
	if err != nil {
		fmt.Println(err)
	}

}
