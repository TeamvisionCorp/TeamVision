import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  selectedApi: 0,
  responseCreateDialogShow: false,
  responseAdded: false
}
const getters = {
  selectedApi (state) {
    return state.selectedApi
  },
  responseCreateDialogShow (state) {
    return state.responseCreateDialogShow
  },
  responseAdded (state){
    return state.responseAdded
  }
}
const mutations = {
  setSelectedApi (state, api) {
    state.selectedApi = api
  },

  setResponseCreateDialogShow (state, show) {
    state.responseCreateDialogShow = show
  },

  setResponseAdded (state, added){
    state.responseAdded = added
  }
}
const actions = {
  setSelectedApiAction (context, isShow) {
    context.commit('setSelectedApi', isShow)
  },

  setResponseCreateDialogShowAction (context, isShow) {
    context.commit('setResponseCreateDialogShow', isShow)
  },

  setResponseAddedAction (context, added) {
    context.commit('setResponseAdded', added)
  }
}
const modules = {}

export default {
  namespaced: true,
  actions,
  getters,
  state,
  mutations,
  modules
}
