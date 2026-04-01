<template>
  <Dialog v-model="show" :options="{ size: '3xl' }">
    <template #body>
      <div class="bg-surface-modal px-4 pb-6 pt-5 sm:px-6">
        <div class="mb-5 flex items-center justify-between">
          <div>
            <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
              {{ __('Create CRM Doc') }}
            </h3>
          </div>
          <div class="flex items-center gap-1">
            <Button
              variant="ghost"
              class="w-7"
              @click="openQuickEntryModal"
            >
              <EditIcon class="h-4 w-4" />
            </Button>
            <Button variant="ghost" class="w-7" @click="show = false">
              <FeatherIcon name="x" class="h-4 w-4" />
            </Button>
          </div>
        </div>

        <!-- Dynamic Fields -->
        <FieldLayout
          v-if="tabs.data?.length"
          :tabs="tabs.data"
          :data="doc.doc"
          doctype="CRM Doc"
        />

        <ErrorMessage v-if="error" class="mt-4" :message="error" />
      </div>

      <div class="px-4 pb-7 pt-4 sm:px-6">
        <div class="flex flex-row-reverse gap-2">
          <Button
            variant="solid"
            :label="__('Create')"
            :loading="loading"
            @click="createDoc"
          />
          <Button
            variant="ghost"
            :label="__('Edit Full Form')"
            @click="openFullForm"
          />
        </div>
      </div>
    </template>
  </Dialog>
</template>


<script setup>
import EditIcon from '@/components/Icons/EditIcon.vue'
import FieldLayout from '@/components/FieldLayout/FieldLayout.vue'
import { usersStore } from '@/stores/users'
import { statusesStore } from '@/stores/statuses'
import { isMobileView } from '@/composables/settings'
import { showQuickEntryModal, quickEntryProps } from '@/composables/modals'
import { useDocument } from '@/data/document'
import { capture } from '@/telemetry'
import { Switch, createResource } from 'frappe-ui'
import { computed, ref, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'

const show = defineModel()
const router = useRouter()

const error = ref(null)
const loading = ref(false)

const { document } = useDocument('CRM Doc')
const doc = document.doc

const tabs = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_fields_layout',
  cache: ['QuickEntry', 'CRM Doc'],
  params: { doctype: 'CRM Doc', type: 'Quick Entry' },
  auto: true,
})
console.log("Tabs : ",tabs)
function createDoc() {
  error.value = null

  loading.value = true
  console.log("Name:", doc.doc.type1)
  createResource({
    url: 'crm.fcrm.doctype.crm_doc.crm_doc.create_crm_doc',
    params: {
      args: {
        doc:doc
      },
    },
    auto: true,
    onSuccess(name) {
      loading.value = false
      show.value = false
      router.push({ name: 'CRM Doc', params: { crmDocId: name } })
      
    },
    onError(err) {
     loading.value = false
      if (err?.messages?.length) {
       error.value = err.messages.join('\n')
      }
      else if (err?.message) {
       error.value = err.message
      }
      else {
       error.value = __('Something went wrong')
      }
    }
  })
}

function openFullForm() {
  router.push({
    name: 'CRMDocID',
    params: {
      docId: doc.doc?.name || 'new'
    }
  })
}

onMounted(() => {
  doc.doc = {}
})


</script>
