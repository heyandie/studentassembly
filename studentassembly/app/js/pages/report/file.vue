<template lang="jade">
section.page__wrapper
  .u-div-180(style="background-color:#293757;")
    .u-bg-img(style="opacity:0.1;background-image:url('/static/img/report-header.jpg');")
section.page__wrapper
  .content__wrapper
    .content__section
      article.content__main
        .u-pos-rel.u-mg-t-180-n
          h1.u-c-white File a Report
          .form__wrapper
            form(@submit.prevent="showConfirmModal = true", enctype="multipart/form-data")
              .form__element(:class="error.school ? 'form--empty' : ''")
                .form__label School
                .form__select
                  v-dropdown(name="school", placeholder="Find your school...", :init-value="$route.query.school", :datalist="schools", @value="updateSchool")
                .form__error(v-if="error.school")
                  span {{ error.school }}
              .form__element(:class="error.category ? 'form--empty' : ''")
                .form__label Type of Report
                .form__select
                  v-dropdown(name="category", placeholder="Choose a category..", :datalist="categories", @value="updateCategory")
                .form__error(v-if="error.category")
                  span {{ error.category }}
              .form__element(v-for="(index, question) in questions")
                .form__label {{ question.text }}
                input(@keydown.enter.prevent="true", type="text", name="question-{{ question.id }}", :value="report.answers[index].text", @input="updateAnswer($event, index)")
              .form__element(:class="error.text ? 'form--empty' : ''")
                .form__label Report Details
                textarea(rows="6", name="text", placeholder="State the corruption case in detail.", :value="report.text", @input="updateText")
                .form__error(v-if="error.text")
                  span {{ error.text }}
              .form__element
                .form__label Attachments
                .form__note It can either be an image or a PDF document. Each file has a 3MB limit.
                .form__attachments
                  template(v-for="index in [0,1,2]")
                    .form__attachment
                      input(type="file", id="file{{ index + 1 }}", accept="image/*,application/pdf,text/pdf", name="files[]", @change="updateAttachment($event, index)", :disabled="filesLengthLessThan(index)")
                      label(for="file{{ index + 1 }}")
                        template(v-if="filesLengthGreaterThan(index)")
                          | {{ report.files[index].name }}
                          .form__attachment__preview(:style="{ backgroundImage: 'url(' + report.files[index].blob + ')' }")
                .form__error(v-if="error.attachment")
                  span {{ error.attachment }}
              .form__element
                .form__label Do you want to publish your report?
                .form__note
                  span Agreeing to publish your report does not guarantee its posting. Student Assembly reserves the right to not publish reports that may be damaging / harmful to others.
                  span
                    | &nbsp;Your post will be anonymously posted as
                    strong &nbsp;{{ alias }}
                    | .
                .form__radio
                  input(type="radio", name="allow_publish", id="allow_publish_1", value="1", @change="updateAllowPublish")
                  label(for="allow_publish_1") Yes, publish my report.
                .form__radio
                  input(type="radio", name="allow_publish", id="allow_publish_2", value="0", @change="updateAllowPublish", checked)
                  label(for="allow_publish_2") No, don't publish my report.
              .form__element
                .form__label Are you willing to provide your contact details?
                .form__note
                  | If this is a
                  strong &nbsp;sexual harassment
                  | &nbsp;or
                  strong &nbsp;discrimination
                  | &nbsp;report and you would like to pursue legal action, kindly give your contact information.
                .form__radio
                  input(type="radio", name="allow_contact", id="allow_contact_1", value="1", @change="updateAllowContact")
                  label(for="allow_contact_1") Yes, I want to give my contact details.
                .form__radio
                  input(type="radio", name="allow_contact", id="allow_contact_2", value="0", @change="updateAllowContact", checked)
                  label(for="allow_contact_2") No, I don't want to give my contact details.
                template(v-if="contact.allow_contact === 1")
                  input(type="text", name="name", placeholder="Name", :value="contact.name", @input="updateName")
                  input(type="text", name="mobile_number", placeholder="Mobile Number", :value="contact.contact_number", @input="updateContact")
              .form__element
                button(type="submit", :disabled="loading")
                  span(v-show="!loading") Submit
                  v-spinner(v-show="loading", :on-button="true", color="#fff", radius="7")
      aside.content__secondary.content--additional-info
        h4
          img(src="/static/img/icons/action/ic_lightbulb_outline_24px.svg", height="18")
          span Some Tips
        ul
          li
            p.small Put the appropriate category so we can place your report properly.
          li
            p.small By entering more relevant details in your report, you are increasing the chances of action being taken:
            ul
              li
                p.small Name and designation of the people responsible
              li
                p.small Date, time, and location of the incident

v-modal(:show.sync="showConfirmModal")
  div(slot="content", style="width:320px;")
    i.modal-close.icon.ion-android-close(@click="showConfirmModal = false")
    h3 Do you want to submit the report?
    p.small You will not be able to edit the report; however, you can add updates about its situation.
    button(type="submit", @click.prevent="submitThenClose()") Submit report
</template>

<script>
import Modal from '../../components/modal.vue'
import Dropdown from '../../components/dropdown.vue'
import Spinner from '../../components/spinner.vue'
import { getProfile } from '../../vuex/actions/user'
import { getSchools, getCategories, submitReport } from '../../vuex/actions/report'

export default {
  vuex: {
    getters: {
      loading: ({ report }) => report.buttonLoading,
      error: ({ report }) => report.error,
      alias: ({ user }) => user.alias,
      schools: ({ report }) => report.schools,
      categories: ({ report }) => report.categories,
      questions: ({ report }) => report.questions,
      report: ({ report }) => report.request.report,
      contact: ({ report }) => report.request.contact
    },
    actions: {
      getProfile,
      getSchools,
      getCategories,
      submitReport,
      updateSchool: ({ dispatch }, value) => {
        console.log(value)
        dispatch('REPORT_UPDATE_REPORT_FIELD', 'school', value)
      },
      updateCategory: ({ dispatch }, value) => {
        dispatch('REPORT_UPDATE_REPORT_FIELD', 'category', value)
        dispatch('REPORT_UPDATE_QUESTIONS')
      },
      updateAnswer: ({ dispatch }, e, index) => {
        dispatch('REPORT_UPDATE_ANSWER', index, e.target.value)
      },
      updateText: ({ dispatch }, e) => {
        dispatch('REPORT_UPDATE_REPORT_FIELD', 'text', e.target.value)
      },
      updateAttachment: ({ dispatch, state }, e, index) => {
        let file = e.target.files[0] || e.dataTransfer.files[0]
        if (file.size < 3145728) {
          let reader = new FileReader()
          reader.onload = () => {
            let fileObject = {
              name: file.name,
              type: file.type,
              size: file.size,
              blob: reader.result
            }
            dispatch('REPORT_SHOW_ERROR', 'attachment', null)
            dispatch('REPORT_UPDATE_ATTACHMENT', parseInt(index), fileObject)
          }
          reader.readAsDataURL(file)
        }
        else {
          dispatch('REPORT_SHOW_ERROR', 'attachment', file.name + ' is bigger than 3MB. Upload a smaller version.')
        }
      },
      updateAllowPublish: ({ dispatch }, e) => {
        dispatch('REPORT_UPDATE_REPORT_FIELD', 'allow_publish', parseInt(e.target.value))
      },
      updateAllowContact: ({ dispatch }, e) => {
        dispatch('REPORT_UPDATE_CONTACT_FIELD', 'allow_contact', parseInt(e.target.value))
      },
      updateName: ({ dispatch }, e) => {
        dispatch('REPORT_UPDATE_CONTACT_FIELD', 'name', e.target.value)
      },
      updateContact: ({ dispatch }, e) => {
        dispatch('REPORT_UPDATE_CONTACT_FIELD', 'contact_number', e.target.value)
      },
      clearForm: ({ dispatch }) => {
        dispatch('REPORT_CLEAR_ERRORS')
        dispatch('REPORT_CLEAR_FIELDS')
      }
    }
  },
  data () {
    return {
      showConfirmModal: false
    }
  },
  methods: {
    submitThenClose () {
      this.showConfirmModal = false
      this.submitReport(this)
    },
    filesLengthLessThan (index) {
      return this.report.files.length < index
    },
    filesLengthGreaterThan (index) {
      return this.report.files.length > index
    }
  },
  created () {
    this.clearForm()
    this.getProfile()
    this.getSchools(this)
    this.getCategories(this)
  },
  components: {
    'v-modal': Modal,
    'v-dropdown': Dropdown,
    'v-spinner': Spinner
  }
}
</script>
