<template>
  <div class="bg-black ps-3">
    <div class="row">
      <div class="col">
        <button 
          class="btn" type="submit" id="btn-1m"
          :class="{ 'btn-success': interval == '1m',  'text-white': interval != '1m' }"
          style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .3rem; --bs-btn-font-size: .55rem; background-color:transperent;"
          @click="change_interval('1m')"
        >1m</button>
        <button 
          class="btn" type="submit" id="btn-30m"
          :class="{ 'btn-success': interval == '30m',  'text-white': interval != '30m' }"
          style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .3rem; --bs-btn-font-size: .55rem; background-color:transperent;"
          @click="change_interval('30m')"
        >30m</button>
        <button 
          class="btn" type="submit" id="btn-1h"
          :class="{ 'btn-success': interval == '1h',  'text-white': interval != '1h' }"
          style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .3rem; --bs-btn-font-size: .55rem; background-color:transperent;"
          @click="change_interval('1h')"
        >1h</button>
        <button 
          class="btn" type="submit" id="btn-4h"
          :class="{ 'btn-success': interval == '4h',  'text-white': interval != '4h' }"
          style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .3rem; --bs-btn-font-size: .55rem; background-color:transperent;"
          @click="change_interval('4h')"
        >4h</button>
        <button 
          class="btn" type="submit" id="btn-1d"
          :class="{ 'btn-success': interval == '1d',  'text-white': interval != '1d' }"
          style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .3rem; --bs-btn-font-size: .55rem; background-color:transperent;"
          @click="change_interval('1d')"
        >1d</button>
      </div>
      <div class="col-2">
        <h3 class="text-center" :class="{ 'text-danger': !is_text_green,  'text-success': is_text_green }">{{ price_change }}</h3>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <apexchart type="candlestick" ref="realtimeChart" height="350" :options="chartOptions" :series="series" :key="updateKey"></apexchart>
    </div>
  </div>
</template>

<script>
import axios from 'axios';


export default {
  name: 'chart',
  props: ['currency'],
  data() {
    return {
      price_change: '',
      volume: '',
      updateKey: 1,
      parse_intervals: {'1m': 60000, '30m': 15*60*1000, '1h': 25*60*1000, '4h': 35*60*1000, '1d': 2*60*60*1000},
      interval: '1h',
      timer: null,
      timer2: null,
      chartOptions: {
        chart: {
          type: 'candlestick',
          height: 350,
          toolbar: {
            show: false
          },
          background: 'black'
        },
        title: {
          text: this.currency,
          align: 'left'
        },
        subtitle: {
          text: 'Volume',
          align: 'left',
          margin: 10,
          offsetX: 0,
          floating: false,
          style: {
            fontSize:  '14px',
            fontWeight:  'normal',
            fontFamily:  undefined,
            color:  '#9699a2'
          },
        },
        xaxis: {
          type: 'datetime',
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false
          }
        },
        yaxis: {
          tooltip: {
            enabled: true
          },
          opposite: true,
        },
        grid: {
          yaxis: {
            lines: {
              show: false
            }
          }
        }
      },
      series: [{
        data: []
      }]
    }
  },
  methods: {
    get_cources() {
      const path = 'http://localhost:5000/cources';
      axios.post(path, {symbol: this.currency, interval: this.interval})
        .then((response) => {
          let new_data = []
          for(let j of response.data.data){
            new_data.push({
              x: new Date(j[0]),
              y: [j[1], j[2], j[3], j[4]]
            })
          }
          this.series = [{ data: new_data }]

          this.timer = setTimeout(() => {
            this.get_cources()
          }, this.parse_intervals[this.interval])
        })
        .catch((error) => {
          console.log('error');
          console.log(error);
            this.timer = setTimeout(() => {
              this.get_cources()
            }, 10000)
        });
    },
    get_24h_change() {
      const path = 'http://localhost:5000/price_change';
      axios.get(path, { params: { currency: this.currency.replace("/", "") } } )
        .then((response) => {
          this.price_change = response.data.persent
          this.volume = response.data.volume
          this.updateKey++
          this.chartOptions.subtitle.text = this.volume

          this.$emit('updateParent', {
            price_change: this.price_change.replace('+', '').replace('%', ''),
            currency: this.currency
          })

          this.timer2 = setTimeout(() => {
            this.get_24h_change()
          }, 300000)
        })
        .catch((error) => {
          console.log('error');
          console.log(error);
            this.timer2 = setTimeout(() => {
              this.get_24h_change()
            }, 10000)
        });
    },
    change_interval(new_interval) {
      clearTimeout(this.timer)
      this.interval = new_interval
      this.get_cources()
    }
  },
  computed: {
    is_text_green: function() {
        return this.price_change.indexOf("+") != -1
    }
  },
  created() {
    this.get_cources();
    this.get_24h_change()
  },
  beforeUnmount() {
    clearTimeout(this.timer)
    clearTimeout(this.timer2)
  }
};
</script>
