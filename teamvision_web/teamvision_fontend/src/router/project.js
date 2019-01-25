
// import EnvServiceWebpart from '../components/APIMockWebpart.vue'
import ProjectHead from '../pages/project/Head.vue'
import PortalHead from '../pages/project/PortalHead.vue'
import EmptyHead from '../components/layout/EmptyBodyHead.vue'

const projectRouter = [
  {
    name: 'projectRoot',
    path: '/project',
    components: {
      default: function () {
        return import('../pages/project/ProjectList.vue')
      },
      bodyhead: PortalHead
    },
    meta: ''
  },
  {
    name: 'projectTask',
    path: '/project/:projectID/task',
    components: {
      default: function () {
        return import('../pages/project/projecttask/ProjectTask.vue')
      },
      bodyhead: ProjectHead
    },
    props: {default: true,bodyhead: true},
    meta: ''
  },
  {
    name: 'projectFortesting',
    path: '/project/:projectID/fortesting',
    components: {
      default: function () {
        return import('../pages/project/project-fortesting/ProjectFortesting.vue')
      },
      bodyhead: ProjectHead
    },
    props: {default: true,bodyhead: true},
    meta: ''
  },
  {
    name: 'projectPlan',
    path: '/project/:projectID/plan',
    components: {
      default: function () {
        return import('../pages/project/plan/ProjectPlan.vue')
      },
      bodyhead: ProjectHead
    },
    props: {default: true,bodyhead: true},
    meta: ''
  },

  {
    name: 'projectIssue',
    path: '/project/:projectID/issue/:issueID',
    components: {
      default: function () {
        return import('../pages/project/issue/ProjectIssue.vue')
      },
      bodyhead: ProjectHead
    },
    props: {default: true,bodyhead: true},
    meta: ''
  },

  {
    name: 'projectIssueMobileUpload',
    path: '/project/issue/:issueID/mobile/upload',
    components: {
      default: function () {
        return import('../pages/project/issue/MobileUpload.vue')
      },
      bodyhead: EmptyHead
    },
    props: {default: true,bodyhead: true},
    meta: ''
  },

  {
    name: 'projectFortestingReport',
    path: '/project/:projectID/fortesting/:fortestingID/report/:reportName',
    components: {
      default: function () {
        return import('../pages/project/project-fortesting/report/Report.vue')
      },
      bodyhead: ProjectHead
    },
    props: {default: true,bodyhead: true},
    meta: ''
  }
]

export {
  projectRouter
}
