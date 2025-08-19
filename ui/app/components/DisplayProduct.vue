<template>
  <div
    class="max-w-md mx-auto my-8 p-6 bg-white border border-gray-200 rounded-lg shadow-md"
  >
    <h2 class="text-2xl font-bold text-gray-900 mb-4">JSON Data</h2>
    <div v-if="product" class="space-y-2">
      <p v-for="(value, key) in product" :key="key" class="text-gray-700">
        <strong class="font-semibold text-gray-900"
          >{{ formatKey(key) }}:
        </strong>
        <a
          v-if="isLink(value)"
          :href="value"
          target="_blank"
          class="text-blue-600 hover:underline"
        >
          {{ value }}
        </a>
        <span v-else-if="isDate(key, value)">
          {{ formatDate(value) }}
        </span>
        <span v-else>
          {{ formatValue(value) }}
        </span>
      </p>
    </div>
    <div v-else class="text-gray-700">No data provided</div>
  </div>
</template>

<script setup>
const props = defineProps({
  product: Object || Undefine,
});

function formatKey(key) {
  // Convert snake_case or camelCase to Title Case
  return key
    .replace(/([A-Z])/g, " $1")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatValue(value) {
  // Handle null, undefined, or empty values
  if (value === null || value === undefined || value === "") return "N/A";
  return value;
}

function isDate(key, value) {
  // Check if the key suggests a date and the value is a valid date string
  if (typeof value !== "string") return false;
  const dateKeys = ["created_at", "updated_at", "date"];
  return (
    dateKeys.some((dateKey) => key.toLowerCase().includes(dateKey)) &&
    !isNaN(Date.parse(value))
  );
}

function formatDate(value) {
  if (!value) return "N/A";
  const date = new Date(value);
  return isNaN(date.getTime())
    ? "N/A"
    : date.toLocaleString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
}

function isLink(value) {
  // Basic check for URLs (http, https, ftp)
  return (
    typeof value === "string" &&
    /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i.test(value)
  );
}
</script>
