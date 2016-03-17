<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      article.content__main
        h1 File a report
        .form__wrapper
          form(action="/api/report" method="post" enctype="multipart/form-data")
            .form__element
              .form__label School
              .form__select
                select(name="school" v-model="request.report.school" number)
                  option(disabled selected hidden value="0") Choose a school...
                  option(v-for="school in schools" value="{{ school.id }}") {{ school.name }}
            .form__element
              .form__label Type of Report
              .form__select
                select(name="category" v-model="request.report.category" number)
                  option(disabled selected hidden value="0") Choose a category..
                  option(v-for="category in categories" value="{{ category.id }}") {{ category.name }}
            .form__element
              .form__label Report Details
              textarea(rows="6" name="text" placeholder="State the corruption case in detail." v-model="request.report.text")
            .form__element
              .form__label Evidences
              .form__note It can either be an image or a document. Each file has a 3MB limit.
              .form__attachments
                .form__attachment
                  input(type="file" id="file1" accept="image/*" name="files[]" v-model="request.report.files[0]")
                  label(for="file1") {{ request.report.files[0] }}
                .form__attachment
                  input(type="file" id="file2" accept="image/*" name="files[]" v-model="request.report.files[1]")
                  label(for="file2") {{ request.report.files[1] }}
                .form__attachment
                  input(type="file" id="file3" accept="image/*" name="files[]" v-model="request.report.files[2]")
                  label(for="file3") {{ request.report.files[2] }}
            .form__element
              .form__label Do you want to publish your report?
              .form__note
                span Agreeing to publish your report does not guarantee its posting. Student Assembly reserves the right to not publish reports that may be damaging / harmful to others.
                span &nbsp;Your post will be anonymously posted as [username].
              .form__radio
                input(type="radio" name="allow_publish" id="allow_publish_1" value="1" v-model="request.report.allow_publish" number)
                label(for="allow_publish_1") Yes, publish my report.
              .form__radio
                input(type="radio" name="allow_publish" id="allow_publish_2" value="0" checked v-model="request.report.allow_publish" number)
                label(for="allow_publish_2") No, don't publish my report.
            .form__element
              .form__label Are you willing to provide your contact details?
              .form__note If this is a sexual harassment or discrimination report and you would like to pursue legal action, kindly give your contact information.
              .form__radio
                input(type="radio" name="allow_contact" id="allow_contact_1" value="1" v-model="request.contact.allow_contact" number)
                label(for="allow_contact_1") Yes, I would to give my contact.
              .form__radio
                input(type="radio" name="allow_contact" id="allow_contact_2" value="0" checked v-model="request.contact.allow_contact" number)
                label(for="allow_contact_2") No, I don't want to give my contact.
              template(v-if="request.contact.allow_contact === 1")
                input(type="text" name="name" placeholder="Name" v-model="request.contact.name")
                input(type="text" name="mobile_number" placeholder="Mobile Number" v-model="request.contact.mobile_number")
            .form__element
              button(type="submit" @click.prevent="submitReport" v-bind:disabled="loading")
                span(v-show="!loading") Submit
                .button__spinner(v-show="loading")
                  v-spinner(color="#fff" height="6px" width="3px" radius="8px")

      aside.content__secondary
        h3 Sample Report
        .form__wrapper
          h4 School
          p UP Diliman

v-footer
</template>

<script>
var Header = require('../components/header.vue');
var Footer = require('../components/footer.vue');
var Spinner = require('../components/spinner.vue');

module.exports = {
  data: function() {
    return {
      schools: null,
      categories: null,
      loading: false,
      request: {
        contact: {
          allow_contact: false,
          name: null,
          contact_number: null
        },
        report: {
          category: null,
          school: null,
          text: null,
          answers: null,
          files: [],
          allow_publish: false
        }
      }

    }
  },
  methods: {
    // watchFileInput: function() {
    //   var file = event.target.files[0] || event.dataTransfer.files[0];
    //   this.files[ind] = file;
    //   this.fileNames[ind] = event.target.value.split('\\').pop();
    // },
    // notifyFileInput: function(event) {
    //
    // }
    submitReport: function() {
      var that = this;
      that.loading = true;
      client({ path: 'report', entity: this.request }).then(
        function (response) {
          console.log('accepted', response);
          that.loading = false;
        },
        function (response) {
          console.log('rejected', response);
          that.loading = false;
        }
      );
    }
  },
  ready: function() {
    var that = this;
    client({ path: 'schools' }).then(
      function (response) {
        that.schools = response.entity;
      },
      function (response) {
        console.log('Error trying to fetch schools. Contact the server again.');
      }
    );
    client({ path: 'categories' }).then(
      function (response) {
        that.categories = response.entity;
      },
      function (response) {
        console.log('Error trying to fetch categories. Contact the server again.');
      }
    );

    // this.watchFileInput();
  },
  components: {
    'v-header': Header,
    'v-footer': Footer,
    'v-spinner': Spinner
  }
}
</script>
