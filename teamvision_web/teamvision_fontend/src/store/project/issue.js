import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  issueChange: false,
  showIssueDetail: false,
  selectIssueID: 0,
  issueFilters: '',
  searchKeyword: ''
}
const getters = {
  showIssueDetail (state) {
    return state.showIssueDetail
  },

  selectIssueID (state) {
    return state.selectIssueID
  },

  issueChange (state) {
    return state.issueChange
  },

  issueFilters (state) {
    return state.issueFilters
  },

  searchKeyword (state) {
    return state.searchKeyword
  }

}
const mutations = {

  setIssueChange (state, isChange) {
    state.issueChange = isChange
  },

  setIssueFilters (state, filters) {
    state.issueFilters= filters
  },

  setShowIssueDetail (state,isShow) {
    state.showIssueDetail = isShow
  },

  setSelectIssueID (state,issueID) {
    state.selectIssueID = issueID
  },

  setSearchKeyword (state,keyword) {
    state.searchKeyword = keyword
  }

}
const actions = {
  setIssueChangeAction (context, isChanged) {
    context.commit('setIssueChange', isChanged)
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
