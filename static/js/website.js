$(document).ready(function () {
    $("#btn-create-html").click(function (e) {
        fetch('/create_table/')
          .then(resp => resp.blob())
          .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            // the filename you want
            a.download = 'download.html';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            alert('your file has downloaded!'); // or you know, something with better UX...
          })
          .catch(() => alert('oh no!'));
    })
})