const openButtons = document.querySelectorAll('.image');
const popups = document.querySelectorAll('.popup');
const closeButtons = document.querySelectorAll('.closeButton');

openButtons.forEach((openButton, index) => {
    openButton.addEventListener('click', () => {
        popups[index].style.display = 'block';
    });

    closeButtons[index].addEventListener('click', () => {
        popups[index].style.display = 'none';
    });
});
