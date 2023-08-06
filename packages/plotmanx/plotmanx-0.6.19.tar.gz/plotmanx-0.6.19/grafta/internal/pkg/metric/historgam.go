package metric

import (
	"github.com/prometheus/client_golang/prometheus"
)

// Here we assume that our balance endpoint usually take between
// 30~220ms and we design our buckets accordingly.
func responseDurationHistogram() *prometheus.HistogramVec {
	return prometheus.NewHistogramVec(prometheus.HistogramOpts{
		Namespace: "client",
		Name:      "balance_response_duration_histogram",
		Help:      "Balance response duration (ms)",
		Buckets:   []float64{10, 50, 90, 130, 170, 210, 250, 290, 330},
		// This is same as prometheus.LinearBuckets(10, 40, 9)
		// 9 buckets starting from 10 increased by 40
	}, []string{"operation"})
}

// Another example:
// 4 buckets starting from 1 multiplied by 3 between. e.g. 1, 3, 9, 27
// prometheus.ExponentialBuckets(1, 3, 9)