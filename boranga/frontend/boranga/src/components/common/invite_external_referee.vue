<template lang="html">
    <div id="invite-external-referee">
        <modal :title="title()" large ok-text="Send Invite" @ok="validateForm">
            <form
                id="inviteExternalRefereeForm"
                class="needs-validation form-horizontal"
                name="inviteExternalRefereeForm"
                novalidate
            >
                <div class="row mt-3">
                    <div class="col-lg-12 ps-5 pe-5">
                        <alert
                            v-if="errors"
                            class="d-flex align-items-center"
                            type="danger"
                            icon="exclamation-triangle-fill"
                        >
                            {{ errors }}
                        </alert>

                        <div class="row mb-3">
                            <label for="email" class="col-sm-3 col-form-label"
                                >Email
                            </label>
                            <div class="col-sm-9">
                                <input
                                    ref="Email"
                                    v-model="external_referee_invite.email"
                                    type="email"
                                    class="form-control"
                                    name="email"
                                    required
                                />
                                <div class="invalid-feedback">
                                    Please enter a valid email address.
                                </div>
                            </div>
                        </div>

                        <div class="row mb-3 mt-3">
                            <label
                                for="first_name"
                                class="col-sm-3 col-form-label"
                                >First Name</label
                            >
                            <div class="col-sm-9">
                                <input
                                    id="first_name"
                                    ref="first_name"
                                    v-model="external_referee_invite.first_name"
                                    type="text"
                                    class="form-control"
                                    name="first_name"
                                    required
                                />
                                <div class="invalid-feedback">
                                    Please enter the referee's first name.
                                </div>
                            </div>
                        </div>

                        <div class="row mb-3">
                            <label
                                for="last_name"
                                class="col-sm-3 col-form-label"
                                >Last Name</label
                            >
                            <div class="col-sm-9">
                                <input
                                    v-model="external_referee_invite.last_name"
                                    type="text"
                                    class="form-control"
                                    name="last_name"
                                    required
                                />
                                <div class="invalid-feedback">
                                    Please enter the referee's last name.
                                </div>
                            </div>
                        </div>

                        <div class="row mb-4">
                            <label for="mobile" class="col-sm-3 col-form-label"
                                >Invite Comments</label
                            >
                            <div class="col-sm-9">
                                <textarea
                                    v-model="
                                        external_referee_invite.invite_text
                                    "
                                    class="form-control"
                                    name="invite_text"
                                    required
                                />
                                <div class="invalid-feedback">
                                    Please enter an invite comment.
                                </div>
                            </div>
                        </div>

                        <alert class="alert alert-primary">
                            <symbol
                                id="info-fill"
                                fill="currentColor"
                                viewBox="0 0 16 16"
                            >
                                <path
                                    d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"
                                />
                            </symbol>
                            <ul class="list-group">
                                <svg
                                    class="bi flex-shrink-0 text-primary mb-3"
                                    width="24"
                                    height="24"
                                    role="img"
                                    aria-label="Info:"
                                >
                                    <use xlink:href="#info-fill" />
                                </svg>
                                <li class="list-group-item">
                                    When you click 'Send Invite', the external
                                    referee will be sent an invite email.
                                </li>
                                <li class="list-group-item">
                                    They will be asked to create an account to
                                    login and complete their referral.
                                </li>
                            </ul>
                        </alert>
                    </div>
                </div>
            </form>
        </modal>
    </div>
</template>

<script>
import alert from '@vue-utils/alert.vue';
import modal from '@vue-utils/bootstrap-modal.vue';

export default {
    name: 'InviteExternalReferee',
    components: {
        alert,
        modal,
    },
    props: {
        pk: {
            type: Number,
            required: true,
        },
        model: {
            type: String,
            required: true,
        },
        email: {
            type: String,
            required: true,
        },
    },
    emits: ['externalRefereeInviteSent'],
    data: function () {
        return {
            isModalOpen: false,
            external_referee_invite: {
                email: '',
            },
            errors: null,
        };
    },
    watch: {
        isModalOpen: function (val) {
            if (val) {
                this.$nextTick(() => {
                    this.$refs.Email.focus();
                });
            }
        },
        email: function (val) {
            this.external_referee_invite.email = val;
        },
    },
    methods: {
        title: function () {
            return 'Invite External Referee';
        },
        close: function () {
            this.isModalOpen = false;
            this.errors = null;
            this.external_referee_invite = {
                email: '',
            };
            document
                .getElementById('inviteExternalRefereeForm')
                .classList.remove('was-validated');
        },
        validateForm: function () {
            let vm = this;
            var form = document.getElementById('inviteExternalRefereeForm');
            if (form.checkValidity()) {
                vm.sendData();
            } else {
                form.classList.add('was-validated');
                $('#inviteExternalRefereeForm')
                    .find(':invalid')
                    .first()
                    .focus();
            }
            return false;
        },
        sendData: function () {
            let vm = this;
            vm.errors = false;
            const url = `/api/${vm.model}/${vm.pk}/external_referee_invite/`;
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(vm.external_referee_invite),
            })
                .then((response) => {
                    swal.fire({
                        title: 'Success',
                        text: 'External referee invite sent',
                        icon: 'success',
                        confirmButtonText: 'OK',
                        customClass: {
                            confirmButton: 'btn btn-primary',
                        },
                    }).then(() => {
                        vm.$emit('externalRefereeInviteSent', response);
                        vm.close();
                    });
                })
                .catch(async (response) => {
                    vm.errors = await response.json();
                });
        },
    },
};
</script>
