(() => {
  const key = 'danny_drinks_admin_token';
  const label = document.createElement('label');
  label.className = 'check';
  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.id = 'remember-device';
  label.append(checkbox, document.createTextNode('記住這台裝置'));
  document.querySelector('#connect').before(label);
  document.querySelector('#login p').textContent = '使用 danny0926 的 Fine-grained Token，只授權 danny0926.github.io 的 Contents：Read and write。勾選記住裝置可在下次自動連接；登出會清除儲存的 Token。';
  window.adminSession = {
    save(token) {try {sessionStorage.removeItem(key);localStorage.removeItem(key);(checkbox.checked ? localStorage : sessionStorage).setItem(key,token);} catch {document.querySelector('#status').textContent += ' 此瀏覽器無法儲存登入資訊。';}},
    clear() {try {sessionStorage.removeItem(key);localStorage.removeItem(key);}catch {}},
    restore() {try {const stored = localStorage.getItem(key) || sessionStorage.getItem(key);if(stored){checkbox.checked=!!localStorage.getItem(key);document.querySelector('#token').value=stored;document.querySelector('#connect').click();}}catch {}}
  };
})();
