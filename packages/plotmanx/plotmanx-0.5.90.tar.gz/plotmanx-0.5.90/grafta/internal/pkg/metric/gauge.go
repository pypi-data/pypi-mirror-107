package metric
 
import (
	"github.com/prometheus/client_golang/prometheus"
)
 
func diskioGauge() prometheus.Gauge {
	return prometheus.NewGauge(prometheus.GaugeOpts{
		Namespace: "plotman",
		Name:      "disk_data",
		Help:      "Current Disk i/o data",
	})
}