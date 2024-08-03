const atkPresets = JSON.parse(document.getElementById('atkPresets').textContent)
const atkPreset = document.querySelector("#AtkPreset");
const atkStats = document.querySelectorAll(".atk-stat");
const atkCheckboxes = document.querySelectorAll(".atk-checkbox")
const atkRaceSelection = document.querySelectorAll(".atk-race-selection")
const atkRaceNone = document.querySelector("#atk-race-none")

const defPresets = JSON.parse(document.getElementById('defPresets').textContent)
const defPreset = document.querySelector("#DefPreset");
const defStats = document.querySelectorAll(".def-stat");
const defCheckboxes = document.querySelectorAll(".def-checkbox")
const defAttachmentSelection = document.querySelectorAll(".def-attachment-selection")
const defAttachmentNone = document.querySelector("#def-attachment-none")
const defRaceSelection = document.querySelectorAll(".def-race-selection")
const defRaceNone = document.querySelector("#def-race-none")

atkPreset.addEventListener("change", applyAtkPreset);
window.addEventListener("load", applyAtkPreset);
defPreset.addEventListener("change", applyDefPreset);
window.addEventListener("load", applyDefPreset);

function applyAtkPreset(event) {
    if (atkPreset.value == 'None') {
        atkStats.forEach(s => s.removeAttribute('readonly'))
    } else {
        const attrs = atkPresets[atkPreset.value];
        for (const stat of atkStats) {
            if (Object.keys(attrs).includes(stat.id)) {
                stat.value = attrs[stat.id]
                stat.setAttribute('readonly', '')
            }
        }
        for (const checkbox of atkCheckboxes) {
            if (Object.keys(attrs).includes(checkbox.id)) {
                checkbox.setAttribute('checked', '')
            } else {
                checkbox.removeAttribute('checked')
            }
        }
        var noneSelected = true;
        for (const option of atkRaceSelection) {
            if (Object.keys(attrs).includes(option.value)) {
                option.setAttribute('selected', '')
                noneSelected = false;
            } else {
                option.removeAttribute('selected')
            }
        }
        if (noneSelected) {
            atkRaceNone.setAttribute('selected', '')
        }
    }
};

function applyDefPreset(event) {
    if (defPreset.value == 'None') {
        defStats.forEach(s => s.removeAttribute('readonly'))
    } else {
        const attrs = defPresets[defPreset.value];
        for (const stat of defStats) {
            if (Object.keys(attrs).includes(stat.id)) {
                stat.value = attrs[stat.id]
                stat.setAttribute('readonly', '')
            }
        }
        for (const checkbox of defCheckboxes) {
            if (Object.keys(attrs).includes(checkbox.id)) {
                checkbox.setAttribute('checked', '')
            } else {
                checkbox.removeAttribute('checked')
            }
        }
        var noneSelected = true;
        for (const option of defAttachmentSelection) {
            if (Object.keys(attrs).includes(option.value)) {
                option.setAttribute('selected', '')
                noneSelected = false;
            } else {
                option.removeAttribute('selected')
            }
        }
        if (noneSelected) {
            defAttachmentNone.setAttribute('selected', '')
        }
        var noneSelected = true;
        for (const option of defRaceSelection) {
            if (Object.keys(attrs).includes(option.value)) {
                option.setAttribute('selected', '')
                noneSelected = false;
            } else {
                option.removeAttribute('selected')
            }
        }
        if (noneSelected) {
            defRaceNone.setAttribute('selected', '')
        }
    }
};
