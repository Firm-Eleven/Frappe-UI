<!--
<template>
  <div class="p-4">
    <div>Form View</div>

    <FormModel />
  </div>
</template> -->

<template>
  <LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs">
        <template #prefix="{ item }">
          <Icon v-if="item.icon" :icon="item.icon" class="mr-2 h-4" />
        </template>
      </Breadcrumbs>
    </template>
  </LayoutHeader>
  <div class="p-4">
    <FormModel v-if="doctype" :doctype="doctype" />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import FormModel from '@/components/Modals/FormModal.vue'
import {
  createResource,
  Breadcrumbs,
  call,
  usePageMeta,
  toast,
} from 'frappe-ui'

const route = useRoute()

function formatDoctype(slug) {
  if (!slug) return ''
  return slug
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

// const doctype = computed(() => {
//   const pathParts = route.path.split('/').filter(Boolean)

//   const slug = pathParts[0] // "crm-doc"
//   return formatDoctype(slug) // "CRM Doc"
// })

const ref_doctype = computed(() => {
  return route.params.doctype
    ? formatDoctype(route.params.doctype)
    : ''
})
const doctype = ref_doctype.value
console.log("Renderform doctype: ", doctype)

const breadcrumbs = computed(() => {
  return [
    {
      label: doctype,
      route: `/${route.params.doctype}/view`
    },
    {
      label: 'New'
    }
  ]
})
</script>
