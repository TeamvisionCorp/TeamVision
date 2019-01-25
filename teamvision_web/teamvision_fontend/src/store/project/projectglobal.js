import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  createDialogShow: false,
  viewDialogShow: false,
  projectVersion: 0,
  project: 0,
  objectChange: false,
  rightSidePanelShow: false,
  taskViewMode: 1
}
const getters = {
  createDialogShow (state) {
    return state.createDialogShow
  },
  viewDialogShow (state) {
    return state.viewDialogShow
  },
  projectVersion (state) {
    return state.projectVersion
  },
  project (state) {
    return state.project
  },
  objectChange (state) {
    return state.objectChange
  },
  rightSidePanelShow (state) {
    return state.rightSidePanelShow
  },

  taskViewMode (state) {
    return state.taskViewMode
  }

}
const mutations = {
  setCreateDialogShow (state, isShow) {
    state.createDialogShow = isShow
  },
  setViewDialogShow (state, isShow) {
    state.viewDialogShow = isShow
  },
  setProjectVersion (state, versionID) {
    state.projectVersion = versionID
  },

  setProject (state, project) {
    state.project = project
  },

  setObjectChange (state, isChange) {
    state.objectChange = isChange
  },

  setRightPanelShow (state, isShow) {
    state.rightSidePanelShow = isShow
  },

  setTaskViewMode (state,mode) {
    state.taskViewMode = mode
  }
}
const actions = {
  setCreateDialogShowAction (context, isShow) {
    context.commit('setCreateDialogShow', isShow)
  },
  setViewDialogShowAction (context, isShow) {
    context.commit('setViewDialogShow', isShow)
  },
  setProjectVersionAction (context, versionID) {
    context.commit('setProjectVersion', versionID)
  },
  setObjectChangeAction (context, isChanged) {
    context.commit('setObjectChange', isChanged)
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
