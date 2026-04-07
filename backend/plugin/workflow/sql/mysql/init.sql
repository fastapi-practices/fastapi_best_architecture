insert into sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values ('workflow.menu', 'Workflow', '/plugins/workflow', 20, 'mdi:workflow', 0, null, null, 1, 1, 1, '', '审批流', null, now(), null);

set @workflow_menu_id = LAST_INSERT_ID();

insert into sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values
('workflow.start', 'WorkflowStartApply', '/plugins/workflow/start', 1, 'mdi:play-circle-outline', 1, '/plugins/workflow/views/start-apply', null, 1, 1, 1, '', null, @workflow_menu_id, now(), null),
('workflow.definition', 'WorkflowDefinition', '/plugins/workflow/definition', 2, 'carbon:flow', 1, '/plugins/workflow/views/definition', null, 1, 1, 1, '', null, @workflow_menu_id, now(), null),
('workflow.todo', 'WorkflowTodo', '/plugins/workflow/my-todo', 3, 'mdi:clipboard-clock-outline', 1, '/plugins/workflow/views/my-todo', null, 1, 1, 1, '', null, @workflow_menu_id, now(), null),
('workflow.apply', 'WorkflowApply', '/plugins/workflow/my-apply', 4, 'mdi:file-document-edit-outline', 1, '/plugins/workflow/views/my-apply', null, 1, 1, 1, '', null, @workflow_menu_id, now(), null),
('workflow.message', 'WorkflowMessage', '/plugins/workflow/message', 5, 'mdi:message-badge-outline', 1, '/plugins/workflow/views/message', null, 1, 1, 1, '', null, @workflow_menu_id, now(), null);

set @workflow_definition_menu_id = (select id from sys_menu where name = 'WorkflowDefinition' limit 1);

insert into sys_menu (title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values
('新增分类', 'AddWorkflowCategory', null, 0, null, 2, null, 'workflow:category:add', 1, 0, 1, '', null, @workflow_definition_menu_id, now(), null),
('修改分类', 'EditWorkflowCategory', null, 0, null, 2, null, 'workflow:category:edit', 1, 0, 1, '', null, @workflow_definition_menu_id, now(), null),
('新增流程', 'AddWorkflowDefinition', null, 0, null, 2, null, 'workflow:definition:add', 1, 0, 1, '', null, @workflow_definition_menu_id, now(), null),
('修改流程', 'EditWorkflowDefinition', null, 0, null, 2, null, 'workflow:definition:edit', 1, 0, 1, '', null, @workflow_definition_menu_id, now(), null);
