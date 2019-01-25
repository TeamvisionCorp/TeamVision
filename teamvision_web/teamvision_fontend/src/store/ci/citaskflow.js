import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  ciTaskFlowCreateDialogShow: false,
  ciTaskFlowSearchKey: '',
  ciTaskFlowAdded: false,
  addedSectionDialogShow: false,
  addedSection: false,
  ciTaskAddedToSection: false,
  ciTaskAddedToSectionDialogShow: false,
  renameSectionDialogShow: false,
  sectionRenamed: false
}
const getters = {

  ciTaskFlowCreateDialogShow (state) {
    return state.ciTaskFlowCreateDialogShow
  },

  ciTaskFlowSearchKey (state) {
    return state.ciTaskFlowSearchKey
  },
  ciTaskFlowAdded (state) {
    return state.ciTaskFlowAdded
  },
  addedSectionDialogShow (state) {
    return state.addedSectionDialogShow
  },
  addedSection (state) {
    return state.addedSection
  },
  ciTaskAddedToSectionDialogShow (state) {
    return state.ciTaskAddedToSectionDialogShow
  },
  ciTaskAddedToSection (state) {
    return state.ciTaskAddedToSection
  },

  renameSectionDialogShow (state) {
    return state.renameSectionDialogShow
  },

  sectionRenamed (state) {
    return state.sectionRenamed
  }
}
const mutations = {

  setCITaskFlowCreateDialogShow (state, isShow) {
    state.ciTaskFlowCreateDialogShow = isShow
  },
  setCITaskFlowSearchKey (state, key) {
    state.ciTaskFlowSearchKey = key
  },

  setCITaskFlowAdded (state, added) {
    state.ciTaskFlowAdded = added
  },
  setAddedSectionDialogShow (state,show) {
    state.addedSectionDialogShow = show
  },
  setAddedSection (state, added) {
    state.addedSection = added
  },
  setCITaskAddedToSectionDialogShow (state,show) {
    state.ciTaskAddedToSectionDialogShow = show
  },
  setCITaskAddedToSection (state, added) {
    state.ciTaskAddedToSection = added
  },

  setRenameSectionDialogShow (state,show) {
    state.renameSectionDialogShow = show
  },
  setSectionRenamed (state, added) {
    state.sectionRenamed = added
  }
}
const actions = {

  setciTaskFlowCreateDialogShowAction (context, isShow) {
    context.commit('setCITaskFlowCreateDialogShow', isShow)
  },

  setCITaskFlowSearchKeyAction (context, key) {
    context.commit('setCITaskFlowSearchKey', key)
  },
  setCITaskFlowAddedAction (context, added) {
    context.commit('setCITaskFlowAdded', added)
  },
  setAddedSectionDialogShowAction (context,show) {
    context.commit('setAddedSectionDialogShow', show)
  },
  setAddedSectionAction (context, added) {
    context.commit('setAddedSection', added)
  },
  setCITaskAddedToSectionDialogShowAction (context,show) {
    context.commit('setCITaskAddedToSectionDialogShow', show)
  },
  setCITaskAddedToSectionAction (context, added) {
    context.commit('setCITaskAddedToSection', added)
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
