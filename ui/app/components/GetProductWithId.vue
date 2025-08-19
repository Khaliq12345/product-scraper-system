<template>
  <div>
    <UForm :state="state" class="space-y-4 m-8" @submit.prevent="getProduct">
      <UFormField label="Enter the Product Id" name="url">
        <UInput
          v-model="state.productId"
          type="text"
          placeholder="product_12345"
          required
          class="w-full"
        />
      </UFormField>

      <UButton
        type="submit"
        :loading="loading"
        size="md"
        block
        class="text-white"
      >
        {{ loading ? "Extraction..." : "Extract" }}
      </UButton>

      <DisplayProduct v-if="product" :product="product" />
    </UForm>
  </div>
</template>

<script setup lang="ts">
const state = reactive({
  productId: "",
});
const loading = ref(false);
const product = ref();

async function getProduct() {
  loading.value = true;
  if (!state.productId) {
    return;
  }
  try {
    const response = await $fetch("/api/get-product", {
      params: {
        product_id: state.productId,
      },
    });
    console.log(response);
    product.value = response.details;
  } catch (error) {
    console.log(`Error - ${error}`);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped></style>
