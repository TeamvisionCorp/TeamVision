import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  taskChange: false,
  taskFilters: {
    status: [],
    owners: [],
    keyword: ''
  },
  taskGanntMaxSize: false
}
const getters = {
  taskChange (state) {
    return state.taskChange
  },

  taskFilters (status) {
    return state.taskFilters
  },

  taskFilterStatus (state) {
    return state.taskFilters.status
  },

  taskFilterOwners (state) {
    return state.taskFilters.owners
  },

  taskFilterKeyword (state) {
    return state.taskFilters.keyword
  },

  taskGanntMaxSize(state) {
    return state.taskGanntMaxSize
  }

}
const mutations = {

  setTaskChange (state, isChange) {
    state.taskChange = isChange
  },

  setTaskFilterStatus (state, status) {
    state.taskFilters.status = status
  },

  setTaskFilterOwners (state, owners) {
    state.taskFilters.owners = owners
  },

  setTaskFilterKeyword (state, keyword) {
    state.taskFilters.keyword = keyword
  },
  setTaskGanntMaxSize (state,isMax) {
    state.taskGanntMaxSize = isMax
  }
}
const actions = {
  setTaskChangeAction (context, isChanged) {
    context.commit('setTaskChange', isChanged)
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
