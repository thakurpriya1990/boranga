<template>
    <div id="ReinstateImage">
        <modal transition="modal fade" @ok="ok()" @cancel="close()" :title="title" :showOK="false" cancelText="Close" large>
            <div id="image-preview" class="container d-flex align-items-center justify-content-center"
                style="min-height:350px;">
                <img v-if="selected_image" :src="selected_image.url" alt="image" class="img-thumbnail w-50">
            </div>
            <alert type="info">
                <i class="bi bi-info-circle-fill"></i> Click an image to preview
            </alert>
            <table class="table table-sm table-hover">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Date Uploaded</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="image in images" @click="selected_image = image" role="button" :class="selected_image == image ? 'selected-row' : '' ">
                        <td><i class="bi bi-image me-3"></i> {{ image.filename }}</td>
                        <td>{{ new Date(image.uploaded_date).toLocaleDateString() }} at {{ new Date(image.uploaded_date).toLocaleTimeString() }}</td>
                        <td>
                            <button @click="confirmReinstateImage(image)" class="btn btn-primary btn-sm"><i
                                    class="bi bi-box-arrow-in-down-left"></i> Reinstate</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'

export default {
    name: 'ReinstateImage',
    props: {
        title: {
            type: String,
            default: 'Reinstate Image'
        },
        imageHistoryUrl: {
            type: String,
            required: true
        },
    },
    emits: ['reinstateImage'],
    data() {
        return {
            isModalOpen: false,
            images: [],
            selected_image: null,
        };
    },
    components: {
        modal,
        alert
    },
    watch: {
        isModalOpen: function (value) {
            if (value) {
                this.fetchImageHistory();
            }
        }
    },
    methods: {
        close: function () {
            this.isModalOpen = false;
        },
        fetchImageHistory: function () {
            fetch(this.imageHistoryUrl)
                .then(response => response.json())
                .then(data => {
                    this.images = data;
                    if (this.images.length > 0) {
                        this.selected_image = this.images[0];
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        },
        confirmReinstateImage: function (image) {
            swal.fire({
                title: 'Reinstate Image',
                text: `Are you sure you want to reinstate ${image.filename}?`,
                icon: 'question',
                showCancelButton: true,
                buttonsStyling: false,
                confirmButtonText: 'Reinstate Image',
                customClass: {
                    confirmButton: 'btn btn-primary',
                    cancelButton: 'btn btn-secondary me-2',
                },
                reverseButtons: true,
            }).then((result) => {
                if (result.isConfirmed) {
                    this.reinstateImage(image);
                }
            });
        },
        reinstateImage: function (image) {
            this.$emit('reinstateImage', image);
        },
    },
    created() {
        this.fetchImageHistory();
    },
}
</script>

<style>
.selected-row {
    background: rgba(51, 170, 51, .5);
}
</style>
