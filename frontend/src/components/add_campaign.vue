<template>
  <div class="form-container">
    <h2 class="form-title">Add Campaign</h2>
    <form @submit.prevent="submitForm" class="form-body">
      <div class="form-group">
        <label for="name">Name</label>
        <input
          type="text"
          id="name"
          class="form-input"
          v-model="formData.name"
          @input="toggleSubmitButton"
          required
        />
      </div>
      <div class="form-group">
        <label for="description">Description</label>
        <textarea
          id="description"
          class="form-textarea"
          v-model="formData.description"
          rows="3"
          required
        ></textarea>
      </div>
      <div class="form-group">
        <label for="start_date">Start Date</label>
        <input
          type="date"
          id="start_date"
          class="form-input"
          v-model="formData.start_date"
          required
        />
      </div>
      <div class="form-group">
        <label for="end_date">End Date</label>
        <input
          type="date"
          id="end_date"
          class="form-input"
          v-model="formData.end_date"
          required
        />
      </div>
      <div class="form-group">
        <label for="budget">Budget</label>
        <input
          type="number"
          id="budget"
          class="form-input"
          v-model="formData.budget"
          @input="toggleSubmitButton"
          required
        />
      </div>
      <div class="form-group">
        <label for="visibility">Visibility</label>
        <select
          id="visibility"
          class="form-select"
          v-model="formData.visibility"
          required
        >
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
      </div>
      <div class="form-group">
        <label for="goals">Goals</label>
        <textarea
          id="goals"
          class="form-textarea"
          v-model="formData.goals"
          rows="3"
          required
        ></textarea>
      </div>
      <button
        type="submit"
        class="form-submit-btn"
        :disabled="!isFormValid"
      >
        Add Campaign
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      formData: {
        name: "",
        description: "",
        start_date: "",
        end_date: "",
        budget: "",
        visibility: "public",
        goals: "",
      },
      isFormValid: false,
    };
  },
  methods: {
    toggleSubmitButton() {
      this.isFormValid =
        this.formData.name.length >= 3 && Number(this.formData.budget) > 0;
    },
    async submitForm() {
      try {
        const response = await axios.post("http://localhost:5000/api/add_campaign", this.formData);
        if (response.status === 200) {
          this.$router.push("/sponsor_dashboard1");
        }
      } catch (error) {
        alert("Error adding campaign: " + (error.response?.data || error.message));
      }
    },
  },
};
</script>

<style scoped>
/* Container Styling */
.form-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Title Styling */
.form-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
}

/* Form Body Styling */
.form-body {
  display: flex;
  flex-direction: column;
}

/* Form Group */
.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
  color: #555;
}

/* Input Fields */
.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  border-color: #007bff;
  outline: none;
}

/* Submit Button */
.form-submit-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.form-submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.form-submit-btn:hover:not(:disabled) {
  background-color: #0056b3;
}
</style>
