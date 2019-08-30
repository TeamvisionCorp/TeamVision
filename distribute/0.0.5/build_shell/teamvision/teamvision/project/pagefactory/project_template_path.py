# coding=utf-8
'''
Created on 2015-10-10

@author: Devuser
'''


class ProjectTaskPath(object):
    left_nav_template_path = "project/left_nav.html"
    sub_nav_template_path = "task/leftsub_nav.html"
    task_page_template_path = "task/task_list_page.html"
    task_list_template_path = "task/task_list_controll.html"
    task_edit_template_path = "task/project_task_edit.html"
    task_option_template_path = "task/project_task_option.html"
    tag_menu_template_path = "task/tagmenu_control.html"
    owner_menu_template_path = "task/ownermenu_control.html"
    project_menu_template_path = "task/projectmenu_control.html"
    project_task_create_dialog = "task/project_task_create_dialog.html"


class ProjectPortalPath(object):
    left_nav_template_path = "project/left_nav.html"
    sub_nav_template_path = "portal/project_portal_leftsub_nav.html"
    portal_index = "portal/project_portal_index.html"
    project_list_template_path = "portal/portal_project_listview.html"
    project_list_control_path = "portal/portal_project_list_control.html"


class ProjectSettingsPath(object):
    left_nav_template_path = "project/left_nav.html"
    sub_nav_template_path = "settings/leftsub_nav.html"
    project_basic_template_path = "settings/project_basic.html"
    project_member_template_path = "settings/project_member.html"
    project_member_list_path = "settings/project_member_list.html"
    project_member_menu_path = "settings/project_member_popup_menu.html"
    project_member_role_menu_path = "settings/project_member_role_popup_menu.html"
    project_webhook_template_path = "settings/project_webhook.html"
    project_create_dialog_path = "settings/project_create_dialog.html"
    project_create_form_path = "settings/project_create_form.html"
    project_webhook_form_path = "settings/project_webhook_form.html"
    version_list_page_path = "settings/version_listpage.html"
    version_list_controll_path = "settings/version_list_controll.html"
    module_list_page_path = "settings/module_listpage.html"
    module_list_controll_path = "settings/module_list_controll.html"
    project_member_add_dialog = "settings/project_member_add_dialog.html"


class ProjectDashBoardPath(object):
    left_nav_template_path = "project/left_nav.html"
    activity_template_path = "dash_board/activity.html"
    activity_webpart_path = "dash_board/project_activity_list.html"
    project_item_template_path = "dash_board/dashboard_item.html"


class ProjectStatisticsPath(object):
    left_nav_template_path = "project/left_nav.html"
    index_template_path = "statistics/project_statistics_index.html"
    statistics_webapp = "statistics/project_statistics_webapp.html"
    statistics_chart = "statistics/project_statistics_chart.html"
    statistics_issue_number = "statistics/project_issue_status_analytics.html"


class ProjectFortestingPath(object):
    left_nav_template_path = "project/left_nav.html"
    sub_nav_template_path = "fortesting/leftsub_nav.html"
    fortesting_list_page_path = "fortesting/fortesting_listpage.html"
    fortesting_list_controll_path = "fortesting/fortesting_list_controll.html"
    fortesting_column_controll_path = "fortesting/fortesting_column_controll.html"
    fortesting_column_item = "fortesting/fortesting_column_item.html"
    fortesting_content = "fortesting/project_fortesting_view_content.html"
    fortesting_edit_page_path = "fortesting/project_fortesting_edit_page.html"
    fortesting_create_form_path = "fortesting/project_fortesting_create_form.html"
    fortesting_create_dialog_path = "fortesting/project_fortesting_create_dialog.html"
    fortesting_tester_menu = "fortesting/project_fortesting_tester_popup_menu.html"
    fortesting_confirm_dialog = "fortesting/fortesting_confirm_dialog.html"


class ProjectVersionPath(object):
    left_nav_template_path = "project/left_nav.html"
    sub_nav_template_path = "versions/leftsub_nav.html"
    version_sub_nav_template_path = "versions/version_leftsub_nav.html"
    version_list_page_path = "versions/version_listpage.html"
    version_list_controll_path = "versions/version_list_controll.html"


class ProjectArchivePath(object):
    left_nav_template_path = "project/left_nav.html"
    sub_nav_template_path = "archive/leftsub_nav.html"
    archive_index_page_path = "archive/project_archive_index.html"
    archive_webapp = "archive/project_archive_webapp.html"
    archive_item = "archive/project_archive_item.html"


class ProjectIssuePath(object):
    left_nav_template_path = "project/left_nav.html"
    sub_nav_template_path = "issue/leftsub_nav.html"
    issue_index_page_path = "issue/project_issue_index.html"
    issue_webapp = "issue/project_issue_webapp.html"
    issue_item_list = "issue/project_issue_item_list.html"
    issue_item_controll = "issue/project_issue_item_controll.html"
    issue_filter = "issue/project_issue_filter.html"
    issue_filter_body = "issue/project_issue_filter_body.html"
    issue_detail = "issue/project_issue_detail.html"
    issue_context_menu = "issue/project_issue_context_menu.html"
    issue_create_form_path = "issue/project_issue_create_form.html"
    issue_detail_activity = "issue/project_issue_activity.html"
    issue_create_dialog_path = "issue/project_issue_create_dialog.html"
    issue_upload_attachments_dialog = "issue/project_issue_upload_attachments_dialog.html"
    issue_operation_dialog = "issue/project_issue_operation_dialog.html"
    issue_filter_save_dialog = "issue/project_issue_filter_save_dialog.html"
    issue_filter_menu_items = "issue/project_issue_filter_menu.html"
    issue_attachment_viewer = "issue/project_issue_attachment_viewer.html"
    issue_attachment_viewe_iframe = "issue/project_issue_file_view_iframe.html"


class ProjectCommonControllPath(object):
    project_dropdown_list_path = "common/project_dropdown_list_controll.html"
    platform_dropdown_list_path = "common/platform_dropdown_list_controll.html"
    product_dropdown_list_path = "common/product_dropdown_list_controll.html"
    module_dropdown_list_path = "common/module_dropdown_list_controll.html"
    member_dropdown_list = "common/member_dropdown_list_controll.html"
    version_dropdown_list_path = "common/version_dropdown_list_controlls.html"
    issue_field_dropdown_list = "common/issue_field_dropdown_list_controll.html"
    issue_field_dropdown_menu = "common/issue_detail_dropdown_menu.html"
    member_dropdown_menu = "common/member_dropdown_menu.html"
    team_dropdown_list_path = "common/team_dropdown_list_controll.html"
    team_dropdown_menu = "common/team_dropdown_menu.html"
    module_dropdown_menu = "common/module_dropdown_menu.html"
    version_dropdown_menu = "common/version_dropdown_menu.html"
    issue_upload_menu = "common/issue_upload_dropdown_menu.html"
    user_listbox_path = "common/user_listbox_controll.html"
    header_project_menu_path = "project/header_project_menu.html"
    project_filter_menu_controll = "project/project_filter_menu_control.html"
    header_project_control_path = "project/project_header_menu_control.html"


class ProjectEmailReportPath(object):
    email_bvt_report = "email_report/bvt_report.html"
    email_testprogress_report = "email_report/testprogress_report.html"
    email_testcomplete_report = "email_report/testcomplete_report.html"
