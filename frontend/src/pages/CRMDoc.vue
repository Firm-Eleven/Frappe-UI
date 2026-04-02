<template>
  <!-- Header -->
  <LayoutHeader>
    <template #left-header>
      <ViewBreadcrumbs v-model="viewControls" routeName="CRM Doc" />
    </template>

    <template #right-header>
      <Button variant="solid" :label="__('Create')" @click="goToForm">
        <template #prefix>
          <FeatherIcon name="plus" class="h-4" />
        </template>
      </Button>
    </template>
  </LayoutHeader>

  <!-- Controls -->
  <ViewControls
    ref="viewControls"
    v-model="docs"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="CRM Doc"
    :options="{
      allowedViews: ['list']
    }"
  />

  <!-- List View -->
  <CRMDocListView
    v-if="docs.data && rows.length"
    v-model="docs.data.page_length_count"
    v-model:list="docs"
    :rows="rows"
    :columns="docs.data.columns"
    :options="{
      resizeColumn: true,
      rowCount: docs.data.row_count,
      totalCount: docs.data.total_count
    }"
    @loadMore="() => loadMore++"
    @columnWidthUpdated="() => triggerResize++"
    @updatePageCount="(count) => (updatedPageCount = count)"
  />

  <!-- Empty State -->
  <div v-else class="flex h-full items-center justify-center">
    <div class="flex flex-col items-center gap-3 text-gray-400 text-lg">
      <span>No Records Found</span>
      <Button variant="solid" :label="__('Create')" @click="goToForm">
        <template #prefix>
          <FeatherIcon name="plus" class="h-4" />
        </template>
      </Button>
    </div>
  </div>
</template>

<script setup>
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import CRMDocListView from '@/components/ListViews/CRMDocListView.vue'
import ViewControls from '@/components/ViewControls.vue'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import { timeAgo } from '@/utils'

// Router
const router = useRouter()

// State
const docs = ref({})
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

// Navigate to form
function goToForm() {
  router.push({ name: 'RenderForm', params: { doctype: 'crm-doc' } })
}

const rows = computed(() => {
  const data = docs.value?.data?.data || []

  return data.map((row) => {
    return {
      ...row,
      modified: row.modified ? __(timeAgo(row.modified)) : '',
      creation: row.creation ? __(timeAgo(row.creation)) : ''
    }
  })
})
</script>
