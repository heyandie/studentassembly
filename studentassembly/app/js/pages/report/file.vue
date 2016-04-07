<template lang="jade">
section.page__wrapper
  .content__wrapper
    .content__section
      h1 File a report
      article.content__main
        .form__wrapper
          form(action="/api/report" method="post" enctype="multipart/form-data")
            .form__element(:class="error.school ? 'form--empty' : ''")
              .form__label School
              .form__select
                select(name="school" v-on:change="updateSchool")
                  option(disabled selected hidden value="0") Choose a school...
                  option(v-for="school in schools" value="{{ school.id }}") {{ school.name }}
              .form__error(v-if="error.school")
                span {{ error.school }}
            .form__element(:class="error.category ? 'form--empty' : ''")
              .form__label Type of Report
              .form__select
                select(name="category" v-on:change="updateCategory")
                  option(disabled selected hidden value="0") Choose a category..
                  option(v-for="category in categories" value="{{ category.id }}") {{ category.name }}
              .form__error(v-if="error.category")
                span {{ error.category }}
            .form__element(v-for="(index, question) in questions")
              .form__label {{ question.text }}
              input(type="text" name="question-{{ question.id }}" v-bind:value="report.answers[index].text" @input="updateAnswer($event, index)")
            .form__element(:class="error.text ? 'form--empty' : ''")
              .form__label Report Details
              textarea(rows="6" name="text" placeholder="State the corruption case in detail." v-bind:value="report.text" @input="updateText")
              .form__error(v-if="error.text")
                span {{ error.text }}
            .form__element
              .form__label Attachments
              .form__note It can either be an image or a PDF document. Each file has a 3MB limit.
              .form__attachments
                template(v-for="index in [0,1,2]")
                  .form__attachment
                    input(type="file" id="file{{ index + 1 }}" accept="image/*,application/pdf,text/pdf" name="files[]" v-on:change="updateAttachment($event, index)" v-bind:disabled="filesLengthLessThan(index)")
                    label(for="file{{ index + 1 }}")
                      template(v-if="filesLengthGreaterThan(index)")
                        | {{ report.files[index].name }}
                        .form__attachment__preview(v-bind:style="{ backgroundImage: 'url(' + report.files[index].blob + ')' }")
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
                input(type="radio" name="allow_publish" id="allow_publish_1" value="1" v-on:change="updateAllowPublish")
                label(for="allow_publish_1") Yes, publish my report.
              .form__radio
                input(type="radio" name="allow_publish" id="allow_publish_2" value="0" checked v-on:change="updateAllowPublish")
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
                input(type="radio" name="allow_contact" id="allow_contact_1" value="1" v-on:change="updateAllowContact")
                label(for="allow_contact_1") Yes, I want to give my contact details.
              .form__radio
                input(type="radio" name="allow_contact" id="allow_contact_2" value="0" checked v-on:change="updateAllowContact")
                label(for="allow_contact_2") No, I don't want to give my contact details.
              template(v-if="contact.allow_contact === 1")
                input(type="text" name="name" placeholder="Name" v-bind:value="contact.name" @input="updateName")
                input(type="text" name="mobile_number" placeholder="Mobile Number" v-bind:value="contact.contact_number" @input="updateContact")
            .form__element
              button(type="submit" @click.prevent="submitReport(this)" v-bind:disabled="loading")
                span(v-show="!loading") Submit
                .button__spinner(v-show="loading")
                  v-spinner(color="#fff" height="6px" width="3px" radius="8px")

      aside.content__secondary.content--additional-info
        h4
          img(src="/static/img/icons/action/ic_lightbulb_outline_24px.svg" height="18")
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
</template>

<script>
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
      updateSchool: ({ dispatch }, e) => {
        dispatch('REPORT_UPDATE_REPORT_FIELD', 'school', parseInt(e.target.value))
      },
      updateCategory: ({ dispatch }, e) => {
        dispatch('REPORT_UPDATE_REPORT_FIELD', 'category', parseInt(e.target.value))
        dispatch('REPORT_UPDATE_QUESTIONS')
      },
      updateAnswer: ({ dispatch }, e, index) => {
        dispatch('REPORT_UPDATE_ANSWER', index, e.target.value)
      },
      updateText: ({ dispatch }, e) => {
        dispatch('REPORT_UPDATE_REPORT_FIELD', 'text', e.target.value)
      },
      updateAttachment: ({ dispatch, state }, e, index) => {
        // function imgLoad(file) {
        //   return new Promise((resolve, reject) => {
        //     let reader = new FileReader()
        //     reader.onload = () => {
        //       file.blob = reader.result
        //       resolve(file)
        //     }
        //     reader.readAsDataURL(file)
        //   })
        // }
        // imgLoad(file).then(
        //   (response) => {
        //     dispatch('REPORT_UPDATE_ATTACHMENT', parseInt(index), response)
        //   },
        //   (error) => {
        //     console.log(error)
        //   }
        // )

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
        dispatch('REPORT_CLEAR_FIELDS')
      }
    }
  },
  methods: {
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
    'v-spinner': Spinner
  }
}
</script>
