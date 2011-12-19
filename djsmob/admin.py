#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-
#
# This file is part of AGAVE
#
# AGAVE is distributed under the terms of the BSD License. The full license is in
# the file LICENSE, distributed as part of this software.
#
# Copyright (c) 2010, Digital Enterprise Research Institute (DERI),NUI Galway.
# All rights reserved.
#
# Author: Julia Anaya
# Email: julia dot anaya at gmail dot com
#
# FILE:
# file-name
#
# DESCRIPTION:
# Description
#
# TODO:


from django.contrib import admin
from models import Person, Post


##class ConoceptInline(admin.TabularInline):
##    model = Concept
##    extra = 0
##
##class InstanceActorInline(admin.TabularInline):
##    model = Instance.actors.through
##    extra = 0
##    classes = ['collapse', 'collapsed']
##    readonly_fields = ('instance', 'actor', 'weight')
##
##class BroaderToInline(admin.TabularInline):
##    model = CCb
##    fk_name = "concept_to"
##    extra = 0)
##
##
##class InstanceAdmin(admin.ModelAdmin):
##    readonly_fields = ('pmid', 'title', 'actors', 'concepts')
##    list_display = ('pmid', 'title')#, 'year') #, 'actors')
## #   list_filter = ('pmid','title') #,'actors')
##    search_fields = ['pmid', 'title'] #, 'actors__name', 'Mall__name']
##    ordering = ('title',)
##    inlines = [
##        InstanceActorInline,
##        InstanceConceptInline,
##    ]

##class PersonAdmin(admin.ModelAdmin):
##    pass
##
##admin.site.register(Instance, InstanceAdmin)

admin.site.register(Person)
admin.site.register(Post)