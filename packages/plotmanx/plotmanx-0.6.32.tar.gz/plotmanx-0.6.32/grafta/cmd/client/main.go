package main

import (
	"dshbdipant/internal/controller"
	"dshbdipant/internal/pkg/metric"
	"dshbdipant/internal/pkg/prometheus"
	"log"
	"net/http"
)

func main() {
	log.Println("plotman center server running on :8080")

	// Prometheus
	pro := prometheus.New(true)

	// Metric
	mtr := metric.New(pro.Registry())

	// Router
	rtr := http.NewServeMux()
	rtr.HandleFunc("/metrics", pro.Handler())
	rtr.HandleFunc("/api/v1/balances", controller.NewBalanceUpdate(mtr).Handle)

	// Server
	log.Fatalln(http.ListenAndServe(":8080", rtr))
}
