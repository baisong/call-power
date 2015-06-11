from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)
from flask.ext.login import login_required

import json

from ..extensions import db
from ..utils import choice_items, choice_keys, choice_values_flat

from .constants import CAMPAIGN_NESTED_CHOICES, CUSTOM_CAMPAIGN_CHOICES, EMPTY_CHOICES
from .models import Campaign
from .forms import CampaignForm, CampaignRecordForm, CampaignStatusForm

campaign = Blueprint('campaign', __name__, url_prefix='/admin/campaign')


@campaign.route('/')
@login_required
def index():
    campaigns = Campaign.query.all()
    return render_template('campaign/list.html', campaigns=campaigns)


@campaign.route('/', methods=['GET', 'POST'])
@campaign.route('/<int:campaign_id>/', methods=['GET', 'POST'])
@login_required
def form(campaign_id=None):
    edit = False
    if campaign_id:
        edit = True

    if edit:
        campaign = Campaign.query.filter_by(id=campaign_id).first_or_404()
        form = CampaignForm(obj=campaign)
    else:
        campaign = Campaign()
        form = CampaignForm()

    # for fields with dynamic choices, set to empty here in view
    # will be updated in client
    form.campaign_subtype.choices = choice_values_flat(CAMPAIGN_NESTED_CHOICES)
    form.target_set.choices = choice_items(EMPTY_CHOICES)

    # check request form for campaign_subtype, reset if not present
    if not request.form.get('campaign_subtype'):
        form.campaign_subtype.data = None
    if campaign.call_maximum:
        form.call_limit.data = True

    if form.validate_on_submit():
        form.populate_obj(campaign)

        db.session.add(campaign)
        db.session.commit()

        if edit:
            flash('Campaign updated.', 'success')
        else:
            flash('Campaign created.', 'success')
        return redirect(url_for('campaign.record', campaign_id=campaign.id))

    return render_template('campaign/form.html', form=form, edit=edit,
                           CAMPAIGN_NESTED_CHOICES=CAMPAIGN_NESTED_CHOICES,
                           CUSTOM_CAMPAIGN_CHOICES=CUSTOM_CAMPAIGN_CHOICES)


@campaign.route('/<int:campaign_id>/copy', methods=['GET', 'POST'])
@login_required
def copy(campaign_id):
    orig_campaign = Campaign.query.filter_by(id=campaign_id).first_or_404()
    new_campaign = orig_campaign.duplicate()

    db.session.add(new_campaign)
    db.session.commit()

    flash('Campaign copied.', 'success')
    return redirect(url_for('campaign.form', campaign_id=new_campaign.id))


@campaign.route('/<int:campaign_id>/record', methods=['GET', 'POST'])
@login_required
def record(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first_or_404()
    form = CampaignRecordForm()

    return render_template('campaign/record.html', campaign=campaign, form=form)


@campaign.route('/<int:campaign_id>/status', methods=['GET', 'POST'])
@login_required
def status(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first_or_404()
    form = CampaignStatusForm(obj=campaign)

    if form.validate_on_submit():
        form.populate_obj(campaign)

        db.session.add(campaign)
        db.session.commit()

        flash('Campaign status updated.', 'success')
        return redirect(url_for('campaign.index'))

    return render_template('campaign/status.html', campaign=campaign, form=form)
