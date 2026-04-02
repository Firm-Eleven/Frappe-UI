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

const route = useRoute()

// Convert slug → "CRM Doc"
function formatDoctype(slug) {
  if (!slug) return ''
  return slug
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

// Extract doctype from URL
const doctype = computed(() => {
  // Example: /crm-doc/render-form → ['crm-doc', 'render-form']
  const pathParts = route.path.split('/').filter(Boolean)

  const slug = pathParts[0] // "crm-doc"
  return formatDoctype(slug) // "CRM Doc"
})

const breadcrumbs = computed(() => {
  return [
    {
      label: __('CRM Doc'),
      route: { name: 'CRM Doc' } // list view navigation
    },
    {
      label: __('New') // static
    }
  ]
})
</script>
