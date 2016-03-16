<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      h1 File a report
      .form__wrapper
        form(action="/api/report" method="post" enctype="multipart/form-data")
          .form__element
            .form__label School
            .form__select
              select(name="school" v-model="report.school" number)
                option(disabled selected hidden value="0") Choose a school...
                option(v-for="school in schools" value="{{ school.id }}") {{ school.name }}
          .form__element
            .form__label Type of Report
            .form__select
              select(name="category" v-model="report.category" number)
                option(disabled selected hidden value="0") Choose a category..
                option(v-for="category in categories" value="{{ category.id }}") {{ category.name }}
          .form__element
            .form__label Report Details
            textarea(rows="10" name="text" placeholder="State the corruption case in detail." v-model="report.text")
          .form__element
            .form__label Attachments
            .form__note It can be a document or an image. Each file has a 3MB limit.
            .form__attachments
              .form__attachment
                input(type="file" id="file1" accept="image/*" v-model="file1")
                label(for="file1") {{ file1 }}
              .form__attachment
                input(type="file" id="file2" accept="image/*" v-model="file2")
                label(for="file2") {{ file2 }}
              .form__attachment
                input(type="file" id="file3" accept="image/*" v-model="file3")
                label(for="file3") {{ file3 }}
          .form__element
            .form__label Do you want to publish your report?
            .form__note Agreeing to publish your report does not guarantee its posting. Student Assembly reserves the right to not publish reports that may be damaging / harmful to others.
            .form__radio
              input(type="radio" name="allow_publish" id="allow_publish_1" value="1" v-model="report.allow_publish" number)
              label(for="allow_publish_1") Yes, publish my report.
            .form__radio
              input(type="radio" name="allow_publish" id="allow_publish_2" value="0" checked v-model="report.allow_publish" number)
              label(for="allow_publish_2") No, don't publish my report.
          .form__element
            .form__label Are you willing to provide your contact details?
            .form__note If this is a sexual harassment or discrimination report and you would like to pursue legal action, kindly give your contact information.
            .form__radio
              input(type="radio" name="allow_contact" id="allow_contact_1" value="1" @click="allowContact = true")
              label(for="allow_contact_1") Yes, I would to give my contact.
            .form__radio
              input(type="radio" name="allow_contact" id="allow_contact_2" value="0" @click="allowContact = false" checked)
              label(for="allow_contact_2") No, I don't want to give my contact.
            template(v-if="allowContact")
              input(type="text" placeholder="Name")
              input(type="email" placeholder="Email Address")
              input(type="text" placeholder="Mobile Number")
          .form__element
            button(type="submit" @click.prevent="submitReport" v-bind:disabled="loading")
              span(v-show="!loading") Submit
              .button__spinner(v-show="loading")
                v-spinner(color="#fff" height="6px" width="3px" radius="8px")


</template>

<script>
var Header = require('../components/header.vue');
var Spinner = require('../components/spinner.vue');

module.exports = {
  data: function() {
    return {
      allowContact: false,
      schools: null,
      categories: null,
      file1: null,
      file2: null,
      file3: null,
      loading: false,
      report: {
        category: null,
        school: null,
        text: null,
        answers: null,
        files: [this.file1, this.file2, this.file3],
        allow_publish: false
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
      client({ path: 'report', entity: this.report }).then(
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
    'v-spinner': Spinner
  }
}
</script>
