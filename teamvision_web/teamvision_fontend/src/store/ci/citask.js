import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  ciLogDialogShow: false,
  ciTaskCreateDialogShow: false,
  ciTaskSearchKey: '',
  ciTaskAdded: false
}
const getters = {
  ciLogDialogShow (state) {
    return state.ciLogDialogShow
  },

  ciTaskCreateDialogShow (state) {
    return state.ciTaskCreateDialogShow
  },

  ciTaskSearchKey (state) {
    return state.ciTaskSearchKey
  },
  ciTaskAdded (state) {
    return state.ciTaskAdded
  }
}
const mutations = {
  setCILogDialogShow (state, isShow) {
    state.ciLogDialogShow = isShow
  },

  setCITaskCreateDialogShow (state, isShow) {
    state.ciTaskCreateDialogShow = isShow
  },
  setCITaskSearchKey (state, key) {
    state.ciTaskSearchKey = key
  },

  setCITaskAdded (state, added) {
    state.ciTaskAdded = added
  }
}
const actions = {
  setCILogShowAction (context, isShow) {
    context.commit('setCILogDialogShow', isShow)
  },

  setCITaskCreateDialogShowAction (context, isShow) {
    context.commit('setCITaskCreateDialogShow', isShow)
  },

  setCITaskSearchKeyAction (context, key) {
    context.commit('setCITaskSearchKey', key)
  },
  setCITaskAddedAction (context, added) {
    context.commit('setCITaskAdded', added)
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
