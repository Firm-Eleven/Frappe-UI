<template>
  <LayoutHeader v-if="crmDoc.data">
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs">
        <template #prefix="{ item }">
          <Icon v-if="item.icon" :icon="item.icon" class="mr-2 h-4" />
        </template>
      </Breadcrumbs>
    </template>
  </LayoutHeader>
  <div v-if="crmDoc.data" class="flex h-full overflow-hidden">
    <div class="flex-1 p-4 overflow-y-auto">

      <DataFields
        :doctype=doctype
        :docname="crmDoc.data.name"
        @afterSave="() => crmDoc.reload()"
      />

    </div>  
    
  </div>
  <ErrorPage
    v-else-if="errorTitle"
    :errorTitle="errorTitle"
    :errorMessage="errorMessage"
  />
  <FilesUploader
    v-if="crmDoc.data?.name"
    v-model="showFilesUploader"
    doctype="CRM Doc"
    :docname="crmDoc.data.name"
    @after="
      () => {
        activities?.all_activities?.reload()
        changeTabTo('attachments')
      }
    "
  />
</template>
<script setup>
import ErrorPage from '@/components/ErrorPage.vue'
import Icon from '@/components/Icon.vue'
import DataFields from '@/components/Activities/DataFields.vue'
import ActivityIcon from '@/components/Icons/ActivityIcon.vue'
import EmailIcon from '@/components/Icons/EmailIcon.vue'
import CommentIcon from '@/components/Icons/CommentIcon.vue'
import DetailsIcon from '@/components/Icons/DetailsIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import TaskIcon from '@/components/Icons/TaskIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import WhatsAppIcon from '@/components/Icons/WhatsAppIcon.vue'
import SuccessIcon from '@/components/Icons/SuccessIcon.vue'
import AttachmentIcon from '@/components/Icons/AttachmentIcon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { openWebsite, setupCustomizations, copyToClipboard } from '@/utils'
import FilesUploader from '@/components/FilesUploader/FilesUploader.vue'
import { getView } from '@/utils/view'
import { getSettings } from '@/stores/settings'
import { globalStore } from '@/stores/global'
import { getMeta } from '@/stores/meta'
import { useDocument } from '@/data/document'
import { whatsappEnabled, callEnabled } from '@/composables/settings'
import {
  createResource,
  Breadcrumbs,
  call,
  usePageMeta,
  toast,
} from 'frappe-ui'
import { useOnboarding } from 'frappe-ui/frappe'
import { ref, computed, h, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useActiveTabManager } from '@/composables/useActiveTabManager'

const props = defineProps({
  docId: {
    type: String,
    required: true,
  },
  doctype: {
    type: String,
    required: true,
  },
})
  
const doctype = formatDoctype(props.doctype)  
const { brand } = getSettings()
const { $dialog, $socket, makeCall } = globalStore()
const { doctypeMeta } = getMeta(doctype)

const { updateOnboardingStep, isOnboardingStepsCompleted } =
  useOnboarding('frappecrm')

const route = useRoute()
const router = useRouter()

console.log("Record Vue docid : ",props.docId)
console.log(" Record Vue doctype : ",doctype)

const errorTitle = ref('')
const errorMessage = ref('')

const crmDoc = createResource({
  url: 'crm.api.render_form.get_doc',  // make sure path matches your file
  params: {
    doctype: doctype,
    doc_id: props.docId
  },
  cache: ['crmDoc', doctype, props.docId],

  onSuccess: (data) => {
    errorTitle.value = ''
    errorMessage.value = ''
    console.log("create resource called", data)
    console.log("Doc Name from API:", data.name)

    // Customizations, modals, sockets, etc.
    setupCustomizations(crmDoc, {
      doc: data,
      $dialog,
      $socket,
      router,
      toast,
      updateField,
      createToast: toast.create,
      deleteDoc: deleteDoc,
      resource: {
        crmDoc,
      },
      call,
    })
  },

  onError: (err) => {
    if (err.messages?.[0]) {
      errorTitle.value = __('Not permitted')
      errorMessage.value = __(err.messages?.[0])
    } else {
      router.push({ name: doctype })
    }
  },
})


// Lifecycle hooks
onMounted(() => {
  console.log("Route docId:", props.docId)
  crmDoc.fetch()
})



const reload = ref(false)
const showOrganizationModal = ref(false)
const showFilesUploader = ref(false)
const _organization = ref({})

function updateDoc(fieldname, value, callback) {
  value = Array.isArray(fieldname) ? '' : value

  if (validateRequired(fieldname, value)) return

  createResource({
    url: 'frappe.client.set_value',
    params: {
      doctype: doctype,
      name: props.docId,
      fieldname,
      value,
    },
    auto: true,
    onSuccess: () => {
      crmDoc.reload()
      reload.value = true
      toast.success(__('Doc updated'))
      callback?.()
    },
    onError: (err) => {
      toast.error(__('Error updating doc: {0}', [err.messages?.[0]]))
    },
  })
}

function validateRequired(fieldname, value) {
  let meta = crmDoc.data.fields_meta || {}
  if (meta[fieldname]?.reqd && !value) {
    toast.error(__('{0} is a required field', [meta[fieldname].label]))
    return true
  }
  return false
}

const breadcrumbs = computed(() => {
  // Top level: CRM Doc list
  let items = [
    { 
      label: __(doctype), 
      route: { name: doctype }  // list view route name
    }
  ]

  // Optional view (kanban, table, etc.)
  // if (route.query.view || route.query.viewType) {
  //   let view = getView(route.query.view, route.query.viewType, 'CRM Doc')
  //   if (view) {
  //     items.push({
  //       label: __(view.label),
  //       icon: view.icon,
  //       route: {
  //         name: 'CRM Doc',
  //         params: { viewType: route.query.viewType },
  //         query: { view: route.query.view },
  //       },
  //     })
  //   }
  // }

  // Current record
  items.push({
    label: title.value,
    route: { 
      name: 'CRMDocID',          // record route name
      params: { docId: crmDoc.data?.name } 
    },
  })

  return items
})


const title = computed(() => {
  let t = doctypeMeta[doctype]?.title_field || 'name'
  return crmDoc.data?.[t] || props.docId
})

usePageMeta(() => {
  return {
    title: title.value,
    icon: brand.favicon,
  }
})


function updateField(name, value, callback) {
  updateDoc(name, value, () => {
    crmDoc.data[name] = value
    callback?.()
  })
}

async function deleteDoc(name) {
  await call('frappe.client.delete', {
    doctype: doctype,
    name,
  })
  router.push({ name: doctype })
}

function formatDoctype(path_doctype) {
  return path_doctype
    .replace(/-/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())
}

</script>
