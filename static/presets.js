const trials = document.getElementById("Trials");
const progressBar = document.getElementById("progress");

const atkPresets = JSON.parse(document.getElementById('atkPresets').textContent);
const atkPreset = document.getElementById("AtkPreset");
const atkBattery = document.querySelectorAll(".atkBattery");
const atkStats = document.querySelectorAll(".atk-stat");

const defPresets = JSON.parse(document.getElementById('defPresets').textContent);
const defPreset = document.getElementById("DefPreset");
const defBattery = document.querySelectorAll(".defBattery");
const defStats = document.querySelectorAll(".def-stat");

atkPreset.addEventListener("change", applyAtkPreset);
window.addEventListener("load", applyAtkBattery);
defPreset.addEventListener("change", applyDefPreset);
window.addEventListener("load", applyDefBattery);

function applyAtkBattery() {
    const selectedPreset = atkPreset.selectedOptions[0];

    if (selectedPreset.className == 'atkBattery') {
        progressBar.setAttribute('data-battery', 'true');
        for (const option of defBattery) {
            option.setAttribute('disabled', '');
        }
        for (const stat of atkStats) {
            if (!(selectedPreset.value != "AllAtkPresets" && stat.id == "Atk_Resolve")) {
                stat.setAttribute('disabled', '');
            } else {
                stat.removeAttribute('disabled', '');
            }
        }
        trials.setAttribute('max','1000');
        return true;
    } else {
        return false;
    }
}

function applyAtkPreset() {
    const atkCheckboxes = document.querySelectorAll(".atk-checkbox");
    const atkRaceSelection = document.querySelectorAll(".atk-race-selection");
    const atkRaceNone = document.getElementById("atk-race-none");

    if (!(applyAtkBattery())) {
        progressBar.setAttribute('data-battery', 'false');
        for (const option of defBattery) {
            option.removeAttribute('disabled', '');
        }
        for (const stat of atkStats) {
            stat.removeAttribute('disabled', '');
        }
        trials.setAttribute('max','10000');
        if (atkPreset.value != 'None') {
            const attrs = atkPresets[atkPreset.value];
            for (const stat of atkStats) {
                if (Object.keys(attrs).includes(stat.id)) {
                    stat.value = attrs[stat.id];
                }
            }
            for (const checkbox of atkCheckboxes) {
                if (Object.keys(attrs).includes(checkbox.id)) {
                    checkbox.setAttribute('checked', '');
                } else {
                    checkbox.removeAttribute('checked');
                }
            }
            var noneSelected = true;
            for (const option of atkRaceSelection) {
                if (Object.keys(attrs).includes(option.value)) {
                    option.setAttribute('selected', '');
                    noneSelected = false;
                } else {
                    option.removeAttribute('selected');
                }
            }
            if (noneSelected) {
                atkRaceNone.setAttribute('selected', '');
            }
        }
    }
};

function applyDefBattery() {
    const selectedPreset = defPreset.selectedOptions[0];

    if (selectedPreset.className == 'defBattery') {
        progressBar.setAttribute('data-battery', 'true');
        for (const option of atkBattery) {
            option.setAttribute('disabled', '');
        }
        for (const stat of defStats) {
            if (
                selectedPreset.value == "HPBattery" && stat.id == "Def_HP" ||
                selectedPreset.value == "NimbleBattery" && stat.id != "Def_Resolve" ||
                selectedPreset.value == "AllDefPresets"
            ) {
                stat.setAttribute('disabled', '');
            } else {
                stat.removeAttribute('disabled', '');
            }
        }
        trials.setAttribute('max','1000');
        return true;
    } else {
        return false;
    }
}

function applyDefPreset() {
    const defCheckboxes = document.querySelectorAll(".def-checkbox");
    const defAttachmentSelection = document.querySelectorAll(".def-attachment-selection");
    const defAttachmentNone = document.getElementById("def-attachment-none");
    const defRaceSelection = document.querySelectorAll(".def-race-selection");
    const defRaceNone = document.getElementById("def-race-none");

    if (!(applyDefBattery())) {
        progressBar.setAttribute('data-battery', 'false');
        for (const option of atkBattery) {
            option.removeAttribute('disabled', '');
        }
        for (const stat of defStats) {;
            stat.removeAttribute('disabled', '');
        }
        trials.setAttribute('max','10000');
        if (defPreset.value != 'None') {
            const attrs = defPresets[defPreset.value];
            for (const stat of defStats) {
                if (Object.keys(attrs).includes(stat.id)) {
                    stat.value = attrs[stat.id];
                }
            }
            for (const checkbox of defCheckboxes) {
                if (Object.keys(attrs).includes(checkbox.id)) {
                    checkbox.setAttribute('checked', '');
                } else {
                    checkbox.removeAttribute('checked');
                }
            }
            var noneSelected = true;
            for (const option of defAttachmentSelection) {
                if (Object.keys(attrs).includes(option.value)) {
                    option.setAttribute('selected', '');
                    noneSelected = false;
                } else {
                    option.removeAttribute('selected');
                }
            }
            if (noneSelected) {
                defAttachmentNone.setAttribute('selected', '');
            }
            var noneSelected = true;
            for (const option of defRaceSelection) {
                if (Object.keys(attrs).includes(option.value)) {
                    option.setAttribute('selected', '');
                    noneSelected = false;
                } else {
                    option.removeAttribute('selected');
                }
            }
            if (noneSelected) {
                defRaceNone.setAttribute('selected', '')
            }
        }
    }
};
