import datetime

from django.http import HttpResponse, Http404
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from journal.models import Entry

def _get_queryset(categories=(), date_range=(None, None)):
    # Filter by category
    if len(categories) == 0:
        qs = Entry.objects.all()
    else:
        filter = reduce(lambda a, b: a | b,
                        map(lambda cat: Q(category__slug=cat), categories))
        qs = Entry.objects.filter(filter)

    # Filter by date
    start, last = date_range
    if start is not None and last is not None:
        qs = qs.filter(pub_date__gte=start, pub_date__lt=last)

    return qs

def _paginate(queryset, page, paginate_by):
    p = Paginator(queryset, paginate_by)
    return p.page(page)

def index(request, categories=(), paginate_by=10, template_name=None):
    try:
        queryset = _get_queryset(categories)
        page = int(request.GET.get('page', 1))
        items = _paginate(queryset, page, paginate_by)
    except (ValueError, InvalidPage):
        raise Http404()

    template = 'archive.html'
    if template_name is not None:
        template = '%s_%s' % (template_name, template)
    template = 'journal/%s' % template
    return render_to_response(template, {'items': items},
                              context_instance=RequestContext(request))

def archive_year(request, year, categories=(), paginate_by=10,
                 template_name=None):
    try:
        year = int(year)
        start = datetime.date(year, 1, 1)
        last = datetime.date(year+1, 1, 1)
        queryset = _get_queryset(categories, (start, last))

        page = int(request.GET.get('page', 1))
        items = _paginate(queryset, page, paginate_by)
    except (ValueError, InvalidPage):
        raise Http404()

    template = 'archive_year.html'
    if template_name is not None:
        template = '%s_%s' % (template_name, template)
    template = 'journal/%s' % template
    return render_to_response(template, {'year': year,
                                         'items': items},
                              context_instance=RequestContext(request))

def archive_month(request, year, month, categories=(), paginate_by=10,
                  template_name=None):
    try:
        year, month = int(year), int(month)
        start = datetime.date(year, month, 1)
        if month < 12:
            last = datetime.date(year, month+1, 1)
        else:
            last = datetime.date(year+1, 1, 1)
        queryset = _get_queryset(categories, (start, last))

        page = int(request.GET.get('page', 1))
        items = _paginate(queryset, page, paginate_by)
    except (ValueError, InvalidPage):
        raise Http404()

    template = 'archive_month.html'
    if template_name is not None:
        template = '%s_%s' % (template_name, template)
    template = 'journal/%s' % template
    return render_to_response(template, {'year': year, 'month': start,
                                         'items': items},
                              context_instance=RequestContext(request))

def archive_day(request, year, month, day, categories=(), paginate_by=10,
                template_name=None):
    try:
        year, month, day = int(year), int(month), int(day)
        start = datetime.date(year, month, day)
        last = start + datetime.timedelta(days=1)
        queryset = _get_queryset(categories, (start, last))

        page = int(request.GET.get('page', 1))
        items = _paginate(queryset, page, paginate_by)
    except (ValueError, InvalidPage):
        raise Http404()

    template = 'archive_day.html'
    if template_name is not None:
        template = '%s_%s' % (template_name, template)
    template = 'journal/%s' % template
    return render_to_response(template, {'date': start, 'items': items},
                              context_instance=RequestContext(request))

def entry(request, year, month, day, slug, categories=(), paginate_by=10,
          template_name=None):
    try:
        year, month, day = int(year), int(month), int(day)
        date = datetime.date(year, month, day)
    except ValueError:
        raise Http404()

    try:
        queryset = _get_queryset(categories)
        range = (datetime.datetime.combine(date, datetime.time.min),
                 datetime.datetime.combine(date, datetime.time.max))
        item = queryset.get(pub_date__range=range, slug__exact=slug)
    except ObjectDoesNotExist:
        raise Http404()

    template = 'entry.html'
    if template_name is not None:
        template = '%s_%s' % (template_name, template)
    template = 'journal/%s' % template
    return render_to_response(template, {'date': date, 'entry': item},
                              context_instance=RequestContext(request))
