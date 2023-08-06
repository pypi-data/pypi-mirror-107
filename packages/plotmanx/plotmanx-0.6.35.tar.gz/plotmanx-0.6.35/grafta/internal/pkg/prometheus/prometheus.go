package prometheus

import (
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type Prometheus struct {
	registry *prometheus.Registry
	handler  http.HandlerFunc
}

// New returns a new `Metric` instance. The `custom` helps keeping or discarding
// all the built-in default metrics. If you just want to see your custom metrics
// set it to `true`.
func New(custom bool) Prometheus {
	reg := prometheus.NewRegistry()

	if custom {
		return Prometheus{
			registry: reg,
			handler: func(w http.ResponseWriter, r *http.Request) {
				promhttp.HandlerFor(reg, promhttp.HandlerOpts{}).ServeHTTP(w, r)
			},
		}

	} else {
		return Prometheus{
			registry: reg,
			handler: func(w http.ResponseWriter, r *http.Request) {
				promhttp.Handler().ServeHTTP(w, r)
			},
		}
	}
}

// Handler returns HTTP handler.
func (p Prometheus) Handler() http.HandlerFunc {
	return p.handler
}

// Registry returns `Registry` instance which helps registering the custom metric collectors.
func (p Prometheus) Registry() *prometheus.Registry {
	return p.registry
}
