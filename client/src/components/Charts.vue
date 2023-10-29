<template>
  <div class="flex justify-content-center">
    <Sidebar class="bg-white" v-model:visible="visible" position="right">
        <div class="container-fluid">
            <div class="row g-2">
                <h2>Добавить график</h2>
            </div>
            <div class="row g-2">
                <select class="form-select" aria-label="Default select example" @change="changeCallStatus($event)">
                    <option selected>Выберите валюту</option>
                    <option v-for="cur in all_currencies" :key="cur" v-bind:value="cur.value">{{ cur.text }}</option>
                </select>
            </div>
            <div class="row g-2">
                <button type="button" class="btn btn-light" @click="add_currency">Добавить</button>
            </div>
        </div>
    </Sidebar>
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1"></div>
        <div class="col-lg-10 col-md-10 col-sm-10 col-xs-10">
          <h1 class="text-center">Multi Chart</h1>
        </div>
        <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1">
          <button class="btn" @click="visible = true"><i class="fa fa-bars"></i></button>
        </div>
      </div>
    </div>
  </div>

  <div class="container-fluid my-4">
    <div class="row g-2">
      <div class="col-xs-12 col-sm-6 col-md-6 col-lg-6 pe-2" v-for="(cur, index) in currencies" :key="cur">
        <div class="bg-black ps-3 p-2">
          <div class="row">
            <div class="col-lg-11 col-md-11 col-sm-11 col-xs-11"></div>
            <div class="col-lg-1 col-md-2 col-sm-3 col-xs-3">
              <button type="button" class="btn-close btn-close-white" aria-label="Close" @click="remove_currency(index)"></button>
            </div>
          </div>
          <div class="row">
            <div class="col">
              <chart :currency=cur @updateParent="onUpdateSalary"></chart>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

import Chart from './Chart.vue';

export default {
  data() {
    return {
      all_currencies: [],
      selected_value: '',
      currencies: ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'DOT/USDT'],
      currency_price_change: {},
      visible: false
    };
  },
  components: {
    chart: Chart,
  },
  methods: {
    remove_currency(index) {
      this.currencies.splice(index, 1);
      this.$forceUpdate();
    },
    get_all_pairs() {
      axios.get('http://127.0.0.1:5000/pairs')
        .then((response) => {
          let all_cur = response.data.sort()
          for(let i of all_cur) {
            this.all_currencies.push({ text: i, value: i })
          }
        })
        .catch((error) => {
          console.log('error');
          console.log(error);
        })
    },
    changeCallStatus(event){
      this.selected_value = event.target.value
    },
    add_currency() {
      this.currencies.push(this.selected_value)
    },
    onUpdateSalary(someData) {
      this.currency_price_change[someData.currency] = someData.price_change
      for (let i =0; i < this.currencies.length; i++) {
        for (let j = i+1; j < this.currencies.length; j++) {
          if (this.currency_price_change[this.currencies[i]] < this.currency_price_change[this.currencies[j]]) {
            let val = this.currencies[j]
            this.currencies[j] = this.currencies[i]
            this.currencies[i] = val
          }
        }
      }
    }
  },
  created() {
    this.get_all_pairs();
  }
};
</script>
