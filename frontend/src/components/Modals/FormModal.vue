<template>
  <div>
    <!-- Body -->
    <div class="bg-surface-modal px-4 pb-6 pt-5 sm:px-6">
      <!-- Header -->
      <div class="mb-5 flex items-center justify-between">
        <div>
          <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
            {{ doct }}
          </h3>
        </div>
      </div>

      <!-- Dynamic Fields -->
      <FieldLayout
        v-if="tabs.data?.length"
        :tabs="tabs.data"
        :data="doc.doc"
        doctype="docType"
      />

      <ErrorMessage v-if="error" class="mt-4" :message="error" />
    </div>

    <!-- Footer -->
    <div class="px-4 pb-7 pt-4 sm:px-6">
      <div class="flex flex-row-reverse gap-2">
        <Button
          variant="solid"
          :label="__('Create')"
          :loading="loading"
          @click="createDoc"
        />
        <!-- Footer 
        <Button
          variant="ghost"
          :label="__('Edit Full Form')"
          @click="openFullForm"
        />-->
      </div>
    </div>
  </div>
</template>

<script setup>
import FieldLayout from '@/components/FieldLayout/FieldLayout.vue'
import { useDocument } from '@/data/document'
import { createResource } from 'frappe-ui'
import { getMeta } from '@/stores/meta'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const error = ref(null)
const loading = ref(false)

const props = defineProps({
  doctype: String
})

console.log("doctype:", props.doctype)
const doct = props.doctype
const docType = props.doctype

const { document } = useDocument(docType)
const doc = document.doc

// Fetch Quick Entry Layout
const tabs = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_fields_layout',
  cache: ['QuickEntry', docType],
  params: { doctype: docType, type: 'Quick Entry' },
  auto: true,
})

console.log('Tabs Meta : ',tabs)
// Create Doc
function createDoc() {
  error.value = null
  loading.value = true

  createResource({
    url: 'crm.fcrm.doctype.crm_doc.crm_doc.create_crm_doc',
    params: {
      doctype:docType,
      args: {
        doc: doc.doc
      },
    },
    auto: true,
    onSuccess(name) {
      loading.value = false
      // router.push({ name: 'CRM Doc', params: { crmDocId: name } })
      router.push({
        name: 'CRMDocID',
        params: {
          docId: name
        }
      })
    },
    onError(err) {
      loading.value = false
      if (err?.messages?.length) {
        error.value = err.messages.join('\n')
      } else if (err?.message) {
        error.value = err.message
      } else {
        error.value = __('Something went wrong')
      }
    }
  })
}

// Navigate to full form
function openFullForm() {
  router.push({
    name: 'CRMDocID',
    params: {
      docId: doc.doc?.name || 'new'
    }
  })
}

// Initialize empty doc
onMounted(() => {
  doc.doc = {}
})
</script>
