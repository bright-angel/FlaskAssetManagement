# -*- encoding: utf-8 -*-

"""
@File    :   asset.py
@Time    :   2025/07/20 22:43:55
@Author  :   test233
@Version :   1.0
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..extensions import db
from ..forms import AssetForm,AssetSearchForm
from ..models.asset import Asset

bp = Blueprint("asset", __name__, url_prefix="/asset")


@bp.route("/")
@login_required
def list_assets():
    form = AssetSearchForm(request.args)
    
    # 处理重置操作
    if 'reset' in request.args:
        return redirect(url_for('asset.list_assets'))
    
    # 初始化查询
    query = Asset.query
    
    # 处理搜索条件
    if 'search' in request.args and form.validate():
        name = form.name.data.strip()
        query = query.filter(Asset.name.ilike(f"%{name}%"))
    
    # 处理分页参数
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 100)  # 限制最大值
    
    # 执行分页查询
    pagination = query.paginate(page=page, per_page=per_page)
    

    
    return render_template(
        "asset/list.html",
        pagination=pagination,
        messages=pagination.items,  # 直接使用分页对象的items
        Asset=Asset,
        title="资产列表",
        form=form,
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_asset():
    form = AssetForm()
    if form.validate_on_submit():
        asset = Asset(
            name=form.name.data,
            category=form.category.data,
            value=form.value.data,
            created_by=current_user.id,
        )
        db.session.add(asset)
        db.session.commit()
        flash("Asset created successfully!", "success")
        return redirect(url_for("asset.list_assets"))
    return render_template("form.html", form=form)


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_asset(id):
    asset = Asset.query.get_or_404(id)
    if asset.created_by != current_user.id and not current_user.is_superuser:
        flash("You do not have permission to edit this asset", "danger")
        return redirect(url_for("asset.list_assets"))

    form = AssetForm(obj=asset)
    if form.validate_on_submit():
        form.populate_obj(asset)
        db.session.commit()
        flash("Asset updated successfully!", "success")
        return redirect(url_for("asset.list_assets"))
    return render_template("form.html", form=form, asset=asset)


@bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_asset(id):
    asset = Asset.query.get_or_404(id)
    if asset.created_by != current_user.id:
        flash("You do not have permission to delete this asset", "danger")
        return redirect(url_for("asset.list_assets"))

    db.session.delete(asset)
    db.session.commit()
    flash("Asset deleted successfully!", "success")
    return redirect(url_for("asset.list_assets"))


@bp.route("/batch_delete", methods=["POST"])
@login_required
def batch_delete():
    asset_ids = request.form.getlist("asset_ids")
    if not asset_ids:
        flash("No assets selected", "warning")
        return redirect(url_for("asset.list_assets"))

    Asset.query.filter(
        Asset.id.in_(asset_ids), Asset.created_by == current_user.id
    ).delete()
    db.session.commit()
    flash(f"{len(asset_ids)} assets deleted successfully", "success")
    return redirect(url_for("asset.list_assets"))
