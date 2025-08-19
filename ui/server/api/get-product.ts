export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const product_id = query.product_id;

  const response = await $fetch(`http://127.0.0.1:8000${event.path}`, {
    params: {
      product_id: product_id,
    },
  });

  console.log(response);

  return response;
});
