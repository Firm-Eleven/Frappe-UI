<template>
  <!-- Header -->
  <LayoutHeader>
    <template #left-header>
      <ViewBreadcrumbs v-model="viewControls" :routeName="doctype.value" />
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
    :doctype="doctype"
    :options="{
      allowedViews: ['list']
    }"
  />

  <!-- List View -->
  <SalesInvoiceListView
    v-if="docs.data && rows.length"
    v-model="docs.data.page_length_count"
    v-model:list="docs"
    :rows="rows"
    :columns="docs.data.columns"
    :doctype="doctype"
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
import SalesInvoiceListView from '@/components/ListViews/SalesInvoiceListView.vue'
import ViewControls from '@/components/ViewControls.vue'
import { useRouter, useRoute } from 'vue-router'
import { ref, watch, computed } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import { formatDate, timeAgo, website, formatTime } from '@/utils'

// Router
const router = useRouter()
const route = useRoute()

// State
const docs = ref({})
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

const path_doctype =  getDoctypeFromPath()
const doctype = ref(formatDoctype(path_doctype))
  
// Navigate to form
function goToForm() {
  router.push({ name: 'RenderForm', params: { doctype: path_doctype } })
}

const rows = computed(() => {
  const data = docs.value?.data?.data || []

  return data.map((row) => {
    return {
      ...row,

      modified: row.modified
        ? {
            label: formatDate(row.modified),
            timeAgo: __(timeAgo(row.modified)),
          }
        : '',

      creation: row.creation
        ? {
            label: formatDate(row.creation),
            timeAgo: __(timeAgo(row.creation)),
          }
        : ''
    }
  })
})
function getDoctypeFromPath() {
  const parts = route.path.split('/')
  return parts[1] // ['', 'crm', 'purchase-invoice', 'view']
}
function formatDoctype(path_doctype) {
  return path_doctype
    .replace(/-/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())
}
watch(
  () => route.path,
  () => {
    const newDoctype = formatDoctype(getDoctypeFromPath())
    
    // update doctype
    doctype.value = newDoctype

    // reset data / reload API
    docs.value = {}
    loadMore.value = 1
  }
)
</script>
