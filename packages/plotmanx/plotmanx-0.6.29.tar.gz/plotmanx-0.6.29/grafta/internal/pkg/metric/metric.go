package metric

import (
	"github.com/prometheus/client_golang/prometheus"
)

type Metric struct {
	HTTPResponseCounter       *prometheus.CounterVec
	BalanceActivityCounter    *prometheus.CounterVec
	DiskIoGauge               prometheus.Gauge
	ResponseDurationHistogram *prometheus.HistogramVec
}

func New(registry *prometheus.Registry) Metric {
	m := &Metric{}

	m.HTTPResponseCounter = httpResponseCounter()
	registry.MustRegister(m.HTTPResponseCounter)
	m.BalanceActivityCounter = balanceActivityCounter()
	registry.MustRegister(m.BalanceActivityCounter)

	m.DiskIoGauge = diskioGauge()
	registry.MustRegister(m.DiskIoGauge)

	m.ResponseDurationHistogram = responseDurationHistogram()
	registry.MustRegister(m.ResponseDurationHistogram)

	return *m
}
