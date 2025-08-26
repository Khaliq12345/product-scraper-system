export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const product_url = query.url;
  const force = query.force;

  const response = await $fetch(`http://127.0.0.1:8000${event.path}`, {
    params: {
      url: product_url,
      force: force,
    },
  });

  return response;
});
