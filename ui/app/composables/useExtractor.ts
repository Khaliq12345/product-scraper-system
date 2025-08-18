
export function useExtractor() {
const state = reactive({ url: '' })
  const extract = ref('');
  const loading = ref(false);

  function handleExtract() {
    if (!state.url) {
      extract.value = '';
      return;
    }
 

    loading.value = true;
    extract.value = `Données extraites sur l'URL ${state.url} et enregistrées dans la base de données`;
    loading.value = false;    
  }

  return {
    state,
    extract,
    loading,
    handleExtract
  };
}