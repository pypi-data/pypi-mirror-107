window.addEventListener('DOMContentLoaded', (event) => {
    const qrImage = document.getElementById('qrExample');
    const dark = document.getElementById('id_dark');
    const light = document.getElementById('id_light');
    const scale = document.getElementById('id_scale');
    const form = document.getElementById('qr-settings-form');

    const valueChanged = () => {
        const lightValue = light.value.replace('#', '');
        const darkValue = dark.value.replace('#', '');
        const scaleValue = scale.value;
        console.log(lightValue, darkValue, scaleValue);
        qrImage.src = `http://qrcodeservice.herokuapp.com/?query=exampledata&light=${lightValue}&dark=${darkValue}&scale=${scaleValue}`;
    }

    dark.addEventListener('change', valueChanged);
    light.addEventListener('change', valueChanged);
    scale.addEventListener('change', valueChanged);
    form.addEventListener('reset', () => {
        setTimeout(valueChanged, 1);
    });
});
