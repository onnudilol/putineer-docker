import Vue from 'vue'
import Router from 'vue-router'
import RestaurantList from '@/components/RestaurantList'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'RestaurantList',
      component: RestaurantList
    }
  ]
})
