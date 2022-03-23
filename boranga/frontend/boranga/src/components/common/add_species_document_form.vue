<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div
        class="modal"
        role="dialog"
        aria-labelledby="modalTitle"
        aria-describedby="modalDescription">
        <header class="modal-header" id="modalTitle">
          <slot name="header">Add a new Document for Species {{ species.species_id }}</slot>
          <button type="button" class="btn-close" @click="close" aria-label="Close">x</button>
        </header>

        <section class="modal-body" id="modalDescription">
            <slot name="body">
                <div class="form-group">
                    <label class="left-equal-width-label pull-left" for="category">Document Category</label>
                    <div class="col-sm-9"> 
                        <select id="category"
                                class="form-control"
                                v-model="selectedCategory">
                            <option v-for="category in categories" v-bind:key="category.id">{{ category }}</option>
                        </select>
                    </div>
                </div><br><br>

                <div class="form-group">
                    <label class="left-equal-width-label pull-left" for="uploadmyfile">Choose Document</label>
                    <div class="col-sm-9">
                        <input type="file" id="uploadmyfile" />
                    </div>
                </div><br><br>

                <div class="form-group">
                    <label class="left-equal-width-label pull-left" for="description">Description</label>
                    <div class="col-sm-9">
                        <textarea id="description"
                                  rows="5"
                                  class="form-control"
                                  v-model="description">
                        </textarea><br>
                    </div>
                </div>

                <div class="form-group">
                    <label class="left-equal-width-label pull-left" for="Name">Date Added</label>
                    <div class="col-sm-9">
                          <div>{{ currentDateTime() }}</div><br>
                    </div>
                </div>

                <div class="form-group">
                    <label class="left-equal-width-label pull-left" for="name_reference">Name Reference</label>
                    <div class="col-sm-9">
                      <input type="text"
                            id="name_reference"
                            class="form-control"
                            v-model="name_reference"><br>
                    </div>
                </div>

                <div class="form-group">
                    <label class="left-equal-width-label pull-left" for="genetic">Genetic</label>
                    <div class="col-sm-9">
                      <input type="text"
                            id="genetic"
                            class="form-control"
                            v-model="genetic"><br>
                    </div>
                </div>

                  <div class="form-group">
                    <label class="left-equal-width-label pull-left" for="biology">Biology</label>
                    <div class="col-sm-9">
                      <input type="text"
                            id="biology"
                            class="form-control"
                            v-model="biology"><br>
                    </div>
                </div>

                <div class="form-group">
                    <label class="left-equal-width-label pull-left" for="ecology">Ecology</label>
                    <div class="col-sm-9">
                      <input type="text"
                            id="ecology"
                            class="form-control"
                            v-model="ecology"><br>
                    </div>
                </div>

                  <div class="form-group">
                    <label class="left-equal-width-label pull-left" for="fire">Fire</label>
                    <div class="col-sm-9">
                      <input type="text"
                            id="fire"
                            class="form-control"
                            v-model="fire"><br>
                    </div>
                </div>

                <div class="form-group">
                    <label class="left-equal-width-label pull-left" for="disease">Disease</label>
                    <div class="col-sm-9">
                      <input type="text"
                            id="disease"
                            class="form-control"
                            v-model="disease">
                    </div>
                </div>
            </slot>
        </section>

        <footer class="modal-footer">
          <slot name="footer"></slot>
          <button type="button" class="btn btn-primary" aria-label="Save">
            Save
          </button>
          <button type="button" class="btn btn-primary" @click="close" aria-label="Close">
            Close
          </button>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>

export default {
  name: "AddSpeciesDocument",
  props: {
    species: {
      type: Object,
      required: true,
    },
  },
  data() {
      return {
          selectedCategory: 'High',
          categories: ['High', 'Medium', 'Low'],
          description: '',
          dateFormat: 'DD/MM/YYYY',
          datepickerOptions:{
              format: 'DD/MM/YYYY',
              showClear: true,
              useCurrent: false,
              keepInvalid: true,
              allowInputToggle: true
          },
          entry_date: '',
          name_reference: '',
          genetic: '',
          biology: '',
          ecology: '',
          fire: '',
          disease: '',
      }
  },
  methods: {
    close() {
        this.$emit("close");
    },
    currentDateTime() {
      const current = new Date();
      const date = current.getDate() + "/" + (current.getMonth()+1) + "/" + current.getFullYear()
      const time = current.getHours() + ":" + current.getMinutes()
      const dateTime = date +' at '+ time;

      return dateTime;
    },
  },
  addEventListeners: function() {
    let vm = this;
  },
  mounted () {
      this.currentDateTime()
  }
};
</script>

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    background: rgba(0, 0, 0, 0.1);
    overflow-x: auto;
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 5%;
    left: 50%;
    transform: translate(-50%, 0%);
    width: 50%;
  }

  .modal-header,
  .modal-footer {
    padding: 15px;
    color: #eeeeee;
    background-color: #eeeeee;
  }

  .modal-header {
    position: relative;
    border-bottom: 1px solid #eeeeee;
    color: #eeeeee;
    justify-content: space-between;
  }

  .modal-footer {
    border-top: 1px solid #eeeeee;
    flex-direction: column;
    background-color: #eeeeee;
  }

  .modal-body {
    position: relative;
    padding: 20px 10px;
    background-color: #eeeeee;
  }

  .btn-close {
    position: absolute;
    top: 0;
    right: 0;
    border: none;
    font-size: 20px;
    padding: 10px;
    cursor: pointer;
    font-weight: bold;
    color: #eeeeee;
    background: transparent;
    color: #eeeeee;
  }

  .modal-fade-enter,
  .modal-fade-leave-to {
    opacity: 0;
  }

  .modal-fade-enter-active,
  .modal-fade-leave-active {
    transition: opacity 0.5s ease;
  }

.left-equal-width-label {
  display: block;
  width: 150px;
  background-color: #eeeeee;
}

input[type=text] {
  background-color: #eeeeee;
  color: #eeeeee;
}
</style>
