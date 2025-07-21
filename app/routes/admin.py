# -*- encoding: utf-8 -*-

"""
@File    :   admin.py
@Time    :   2025/07/20 22:44:43
@Author  :   test233
@Version :   1.0
"""

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    Blueprint,
    current_app,
)
from flask_login import login_required, current_user
from ..extensions import db,csrf
from ..forms import UserForm, RoleForm, PermissionForm, UserSearchForm, PermissionSearchForm
from ..models import User, Role, Permission
from ..utils import role_required, permission_required
from copy import deepcopy

bp = Blueprint("admin", __name__, url_prefix="/admin")


# 用户管理视图
@csrf.exempt
@bp.route("/users")
@login_required
@permission_required('admin.user_list')
def user_list():
    form = UserSearchForm(request.args)
    
    # 处理重置操作
    if 'reset' in request.args:
        return redirect(url_for('admin.user_list'))
    
    # 初始化查询
    query = User.query
    
    # 处理搜索条件
    if 'search' in request.args and form.validate():
        username = form.username.data.strip()
        query = query.filter(User.username.ilike(f"%{username}%"))
    
    # 处理分页参数
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 100)  # 限制最大值
    
    # 执行分页查询
    pagination = query.paginate(page=page, per_page=per_page)
    
    # 密码掩码处理
    for user in pagination.items:
        user.password = user.password[:10] + "..." if user.password else ""
    
    return render_template(
        "admin/user/list.html",
        pagination=pagination,
        messages=pagination.items,  # 直接使用分页对象的items
        User=User,
        title="用户列表",
        form=form,
    )


@bp.route("/user/create", methods=["GET", "POST"])
@permission_required('admin.user_create')
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj_exclude(user, exclude=["password", "roles"])
        if form.password.data:
            user.set_password(form.password.data)
        if form.roles.data:
            roles = Role.query.filter(Role.id.in_(form.roles.data)).all()
            user.roles = roles
        db.session.add(user)
        db.session.commit()
        flash("用户创建成功", "success")
        return redirect(url_for("admin.user_list"))
    return render_template("form.html", form=form, title="创建用户")


@bp.route("/user/edit/<int:id>", methods=["GET", "POST"])
@permission_required('admin.user_edit')
def user_edit(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.is_superuser.data = bool(form.is_superuser.data)
        form.populate_obj_exclude(user, exclude=["password", "roles"])
        if form.password.data:
            user.set_password(form.password.data)
        if form.roles.data:
            roles = Role.query.filter(Role.id.in_(form.roles.data)).all()
            user.roles = roles
        db.session.commit()
        flash("用户更新成功", "success")
        return redirect(url_for("admin.user_list"))
    form.roles.data = [role.id for role in user.roles]
    return render_template(
        "form.html", form=form, user=user, title="编辑用户"
    )


# 删除用户
@bp.route("/user/delete/<int:id>", methods=["GET", "POST"])
@permission_required('admin.user_delete')
def user_delete(id):
    user = User.query.get_or_404(id)
    if user == current_user:
        flash("不能删除当前登录用户", "warning")
        return redirect(url_for("admin.user_list"))
    db.session.delete(user)
    db.session.commit()
    flash("用户已删除", "success")
    return redirect(url_for("admin.user_list"))


# 角色管理
@bp.route("/roles")
@login_required
@permission_required('admin.role_list')
def role_list():
    page = request.args.get("page", 1, type=int)
    pagination = Role.query.paginate(page=page, per_page=10)
    messages = pagination.items
    return render_template(
        "admin/role/list.html",
        pagination=pagination,
        messages=messages,
        Role=Role,
        title="角色列表",
    )


@bp.route("/role/create", methods=["GET", "POST"])
@permission_required('admin.role_create')
def role_create():
    form = RoleForm()
    if form.validate_on_submit():
        role = Role()
        form.populate_obj(role)
        for perm_id in form.permissions.data:
            permission = Permission.query.get(perm_id)
            if permission:
                role.permissions.append(permission)
        db.session.add(role)
        db.session.commit()
        flash("角色创建成功", "success")
        return redirect(url_for("admin.role_list"))
    return render_template("form.html", form=form, title="创建角色")


@bp.route("/role/edit/<int:id>", methods=["GET", "POST"])
@permission_required('admin.role_edit')
def role_edit(id):
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        form.populate_obj_exclude(role, exclude=["permissions"])
        if form.permissions.data:
            permissions = Permission.query.filter(
                Permission.id.in_(form.permissions.data)
            ).all()
            role.permissions = permissions
        db.session.commit()
        flash("角色更新成功", "success")
        return redirect(url_for("admin.role_list"))
    form.permissions.data = [perm.id for perm in role.permissions]
    return render_template(
        "form.html", form=form, role=role, title="编辑角色"
    )


@bp.route("/role/delete/<int:id>", methods=["POST"])
@permission_required('admin.role_delete')
def role_delete(id):
    role = Role.query.get_or_404(id)
    # 检查是否有用户关联，如果有则不能删除
    if role.users.count() > 0:
        flash("该角色下有用户，不能删除", "danger")
        return redirect(url_for("admin.role_list"))

    db.session.delete(role)
    db.session.commit()
    flash("角色已删除", "success")
    return redirect(url_for("admin.role_list"))


# 权限管理
# 权限管理
@bp.route("/permissions")
@login_required
@permission_required('admin.permission_list')
def permission_list():

    form = PermissionSearchForm(request.args)  # 从 GET 参数初始化表单
    
    # 处理重置操作
    if 'reset' in request.args:
        return redirect(url_for('admin.permission_list'))  # 重定向到无参URL
    
    # 初始化查询
    query = Permission.query
    
    # 处理搜索验证
    if 'search' in request.args and form.validate():
        search_api = form.api.data.strip()
        if search_api:
            query = query.filter(Permission.endpoint.ilike(f"%{search_api}%"))

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 100)  # 限制最大值
    pagination = query.paginate(page=page, per_page=per_page)
    messages = pagination.items
    return render_template(
        "admin/permission/list.html",
        pagination=pagination,
        messages=messages,
        Permission=Permission,
        title="权限列表",
        form=form,
    )


@bp.route("/permission/create", methods=["GET", "POST"])
@permission_required('admin.permission_create')
def permission_create():
    form = PermissionForm()
    if form.validate_on_submit():
        # 检查是否已存在相同的endpoint和method
        existing = Permission.query.filter_by(
            endpoint=form.endpoint.data
        ).first()

        if existing:
            flash("该权限已存在", "danger")
            return redirect(url_for("admin.permission_create"))

        permission = Permission()
        form.populate_obj(permission)
        db.session.add(permission)
        db.session.commit()
        flash("权限创建成功", "success")
        return redirect(url_for("admin.permission_list"))
    return render_template("form.html", form=form, title="创建权限")


@bp.route("/permission/edit/<int:id>", methods=["GET", "POST"])
@permission_required('admin.permission_edit')
def permission_edit(id):
    permission = Permission.query.get_or_404(id)
    form = PermissionForm(obj=permission)

    if form.validate_on_submit():
        # 检查是否与其他权限冲突
        existing = Permission.query.filter(
            Permission.endpoint == form.endpoint.data,
            Permission.id != id,
        ).first()

        if existing:
            flash("该权限已存在", "danger")
            return redirect(url_for("admin.permission_edit", id=id))
        form.populate_obj(permission)
        db.session.commit()
        flash("权限更新成功", "success")
        return redirect(url_for("admin.permission_list"))
    return render_template(
        "form.html", form=form, permission=permission, title="编辑权限"
    )


@bp.route("/permission/delete/<int:id>", methods=["POST"])
@permission_required('admin.permission_delete')
def permission_delete(id):
    permission = Permission.query.get_or_404(id)
    # 检查是否有角色关联，如果有则不能删除
    if len(permission.roles) > 0:
        flash("该权限已被角色使用，不能删除", "danger")
        return redirect(url_for("admin.permission_list"))

    db.session.delete(permission)
    db.session.commit()
    flash("权限已删除", "success")
    return redirect(url_for("admin.permission_list"))

@bp.route("/user/batch_delete", methods=["POST"])
@permission_required('admin.user_delete')
def batch_user_delete():
    user_ids = request.form.getlist("user_ids[]")
    users = User.query.filter(User.id.in_(user_ids)).all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    flash("用户已删除", "success")
    return redirect(url_for("admin.user_list"))


@bp.route("/user/export_excel", methods=["POST"])
@permission_required('admin.user_export')
def user_export():
    return redirect(url_for("admin.user_list"))
