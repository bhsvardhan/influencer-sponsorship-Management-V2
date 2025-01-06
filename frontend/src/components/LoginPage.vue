<template>
  <div
    class="container vh-100 d-flex flex-column justify-content-center align-items-center"
  >
    <div
      class="bg-light p-5 rounded shadow"
      style="width: 100%; max-width: 500px"
    >
      <h2 class="text-center">{{ isSignUp ? "Sign Up" : "Login" }}</h2>
      <form @submit.prevent="handleForm">
        <!-- Username -->
        <div class="form-group mt-3">
          <label for="username">Username</label>
          <input
            type="text"
            class="form-control"
            id="username"
            placeholder="Enter username"
            v-model="uname"
          />
        </div>

        <!-- Password -->
        <div class="form-group mt-3">
          <label for="password">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            placeholder="Enter password"
            v-model="password"
          />
        </div>

        <!-- Additional Fields for Sign Up -->
        <div v-if="isSignUp" class="mt-3">
          <!-- User Role Selection -->
          <div class="form-group">
            <label for="userType">Register as</label>
            <select class="form-control" id="userType" v-model="userType">
              <option value="sponsor">Sponsor</option>
              <option value="influencer">Influencer</option>
            </select>
          </div>

          <!-- Additional Fields for Influencers -->
          <div v-if="userType === 'influencer'" class="mt-3">
            <div class="form-group">
              <label for="name">Name</label>
              <input
                type="text"
                class="form-control"
                id="name"
                placeholder="Enter name"
                v-model="name"
              />
            </div>
            <div class="form-group">
              <label for="niche">Niche</label>
              <input
                type="text"
                class="form-control"
                id="niche"
                placeholder="Enter niche"
                v-model="niche"
              />
            </div>
            <div class="form-group">
              <label for="category">Category</label>
              <input
                type="text"
                class="form-control"
                id="category"
                placeholder="Enter category"
                v-model="category"
              />
            </div>
            <div class="form-group">
              <label for="reach">Reach</label>
              <input
                type="text"
                class="form-control"
                id="reach"
                placeholder="Enter reach"
                v-model="reach"
              />
            </div>
            <div class="form-group">
              <label for="platformPresence">Platform Presence</label>
              <input
                type="text"
                class="form-control"
                id="platform_presence"
                placeholder="Enter platform presence"
                v-model="platformPresence"
              />
            </div>
            <div class="form-group">
              <label for="phoneNumber">Phone Number</label>
              <input
                type="text"
                class="form-control"
                id="phoneNumber"
                placeholder="Enter phone number"
                v-model="phoneNumber"
              />
            </div>
          </div>

          <!-- Additional Fields for Sponsors -->
          <div v-if="userType === 'sponsor'" class="mt-3">
            <div class="form-group">
              <label for="name">Name</label>
              <input
                type="text"
                class="form-control"
                id="name"
                placeholder="Enter name"
                v-model="name"
              />
            </div>
            <div class="form-group">
              <label for="industry">Industry</label>
              <input
                type="text"
                class="form-control"
                id="industry"
                placeholder="Enter industry"
                v-model="industry"
              />
            </div>
            <div class="form-group">
              <label for="budget">Budget</label>
              <input
                type="text"
                class="form-control"
                id="budget"
                placeholder="Enter budget"
                v-model="budget"
              />
            </div>
          </div>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="btn btn-primary btn-block w-100 mt-4"
          :disabled="!isFormValid"
        >
          {{ isSignUp ? "Sign Up" : "Login" }}
        </button>
      </form>

      <!-- Toggle Between Login and Sign-Up -->
      <div class="text-center mt-3">
        <small class="text-muted">
          {{ isSignUp ? "Already have an account?" : "Don't have an account?" }}
        </small>
        <span
          class="text-primary text-decoration-underline ms-1"
          style="cursor: pointer"
          @click="toggleSignUp"
        >
          {{ isSignUp ? "Login" : "Sign Up" }}
        </span>
      </div>
    </div>

    <!-- Alert -->
    <div
      v-if="showAlert"
      class="alert mt-3"
      :class="[alertClass]"
      role="alert"
      style="max-width: 500px"
    >
      {{ alertMessage }}
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      uname: "",
      password: "",
      name: "",
      isSignUp: false,
      userType: "sponsor", // Default to sponsor
      niche: "",
      category: "",
      reach: "",
      platformPresence: "",
      phoneNumber: "",
      industry: "",
      budget: "",
      showAlert: false,
      alertMessage: "",
      alertClass: "",
    };
  },
  computed: {
    isFormValid() {
      if (!this.uname.trim() || !this.password.trim()) return false;
      if (this.isSignUp) {
        if (
          this.userType === "sponsor" &&
          (!this.name.trim() || !this.industry.trim() || !this.budget.trim())
        ) {
          return false;
        }
        if (
          this.userType === "influencer" &&
          (!this.name.trim() ||
            !this.niche.trim() ||
            !this.category.trim() ||
            !this.reach.trim() ||
            !this.platformPresence.trim() ||
            !this.phoneNumber.trim())
        ) {
          return false;
        }
      }
      return true;
    },
  },
  methods: {
    handleForm() {
      if (this.uname === "prasadrao" && this.password === "lbnm12345") {
        this.$router.push("/admin_dashboard");
        return;
      }
      const endpoint = this.isSignUp
        ? this.userType === "sponsor"
          ? "http://127.0.0.1:5000/sponsor_register"
          : "http://127.0.0.1:5000/influencer_register"
        : "http://127.0.0.1:5000/loginUser";

      const data = this.isSignUp
        ? this.userType === "sponsor"
          ? {
              username: this.uname, // use "username" here
              password: this.password,
              name: this.name,
              industry: this.industry,
              budget: this.budget,
              isAdmin: 2, // Assuming sponsor role is 2
            }
          : {
              username: this.uname, // use "username" here
              password: this.password,
              name: this.name,
              niche: this.niche,
              category: this.category,
              reach: this.reach,
              platform_presence: this.platformPresence,
              phoneNumber: this.phoneNumber,
              isAdmin: 3, // Assuming influencer role is 3
            }
        : {
            username: this.uname, // use "username" here
            password: this.password,
          };

      axios
        .post(endpoint, data)
        .then((response) => {
          this.showAlert = true;
          this.alertClass = "alert-success";
          this.alertMessage = this.isSignUp
            ? "Sign up successful!"
            : "Login successful!";
          if (!this.isSignUp) {
            const role = response.data.Role;
            localStorage.setItem("role", role);
            localStorage.setItem("username", response.data.Name);
            this.$router.push(
              role === 2 ? "/sponsor_dashboard" : "/influencer_dashboard"
            );
          } else {
            this.resetForm();
            this.toggleSignUp();
          }
        })
        .catch((error) => {
          this.showAlert = true;
          this.alertClass = "alert-danger";
          this.alertMessage = this.isSignUp
            ? "Sign up failed. Please try again."
            : "Invalid username or password.";
        });
    },

    toggleSignUp() {
      this.isSignUp = !this.isSignUp;
      this.resetForm();
    },

    resetForm() {
      this.uname = "";
      this.password = "";
      this.name = "";
      this.niche = "";
      this.category = "";
      this.reach = "";
      this.platformPresence = "";
      this.phoneNumber = "";
      this.industry = "";
      this.budget = "";
    },
  },
  logout() {
    localStorage.removeItem("role");
    localStorage.removeItem("username");
    this.$router.push("/login");
  },

  mounted() {
    localStorage.clear();
    axios.get("http://127.0.0.1:5000/logOut");
  },
};
</script>

<style scoped>
.container {
  background: linear-gradient(to right, #4e54c8, #8f94fb);
  width: 100%;
  height: 100vh;
}

.bg-light {
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  padding: 20px;
  border-radius: 15px;
  max-width: none;
  margin: 0 auto; /* Center the form */
}

.form-group {
  margin-bottom: 1rem; /* Add space between each field */
}

.btn-primary {
  background-color: #4e54c8;
  border: none;
}

.btn-primary:hover {
  background-color: #3b3da2;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
