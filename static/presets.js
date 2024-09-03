const trials = document.getElementById("Trials");
// const progressBar = document.getElementById("progress");

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
        // progressBar.setAttribute('data-battery', 'true');
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
        // progressBar.setAttribute('data-battery', 'false');
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
        // progressBar.setAttribute('data-battery', 'true');
        for (const option of atkBattery) {
            option.setAttribute('disabled', '');
        }
        for (const stat of defStats) {
            if (
                selectedPreset.value == "HPBattery" && stat.id == "Def_HP" ||
                selectedPreset.value == "NimbleBattery" && stat.id != "Def_HP" && stat.id != "Def_Resolve" ||
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
        // progressBar.setAttribute('data-battery', 'false');
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

const form = document.getElementById("form");
const progressLabel = document.getElementById("progress-label");
const progressBar = document.getElementById("progress");

form.addEventListener("submit", updateProgress);

function updateProgress () {
    progressBar.classList.remove("invisible")
    // if (progressBar.getAttribute('data-battery') == 'true') {
    //     progressLabel.classList.remove("invisible")
    //     fetch("/?" + new URLSearchParams({
    //         pID: {{ pID }}
    //     }),
    //     {
    //         method: "GET",
    //         headers: {
    //             "X-Requested-With": "XMLHttpRequest"
    //         },
    //     })
    //     .then(function(response) {
    //         response.json().then(function(data) {
    //             // update the appropriate UI components
    //             progressBar.setAttribute('value', data.progress);
    //             progressBar.setAttribute('max', data.max_progress);
    //             progressLabel.innerHTML = data.progress + " of " + data.max_progress + " processed.";
    //             console.log(progressLabel.innerHTML);
    //             setTimeout(updateProgress, 200);
    //         });
    //     });
    // }
}

let stored = localStorage.getItem('theme')
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
if (stored == 'dark') {
    var isLight = false;
} else if (stored == 'light') {
    var isLight = true;
} else {
    if (prefersDark) {
        var isLight = false;
    } else {
        var isLight = true;
    }
}
const html = document.documentElement
const switchTheme = document.getElementById('theme_switcher')
const sun = '<svg viewBox="0 0 16 16"><path fill="currentColor" d="M8 11a3 3 0 1 1 0-6a3 3 0 0 1 0 6zm0 1a4 4 0 1 0 0-8a4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/></svg>'
const moon = '<svg viewBox="0 0 16 16"><g fill="currentColor"><path d="M6 .278a.768.768 0 0 1 .08.858a7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277c.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316a.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71C0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278zM4.858 1.311A7.269 7.269 0 0 0 1.025 7.71c0 4.02 3.279 7.276 7.319 7.276a7.316 7.316 0 0 0 5.205-2.162c-.337.042-.68.063-1.029.063c-4.61 0-8.343-3.714-8.343-8.29c0-1.167.242-2.278.681-3.286z"/><path d="M10.794 3.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387a1.734 1.734 0 0 0-1.097 1.097l-.387 1.162a.217.217 0 0 1-.412 0l-.387-1.162A1.734 1.734 0 0 0 9.31 6.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387a1.734 1.734 0 0 0 1.097-1.097l.387-1.162zM13.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.156 1.156 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.156 1.156 0 0 0-.732-.732l-.774-.258a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732L13.863.1z"/></g></svg>'

document.addEventListener('DOMContentLoaded', () => {
    html.setAttribute('data-theme', isLight? 'light':'dark')
    switchTheme.innerHTML = isLight? sun : moon
    switchTheme.setAttribute('data-tooltip', `${isLight?'Light':'Dark'} theme`)
})
switchTheme.addEventListener('click', (e)=> {
    e.preventDefault()
    isLight = !isLight
    html.setAttribute('data-theme', isLight? 'light':'dark')
    switchTheme.innerHTML = isLight? sun : moon
    switchTheme.setAttribute('data-tooltip', `${isLight?'Light':'Dark'} theme`)
    localStorage.setItem('theme', isLight? 'light':'dark')
    removeTooltip()
})
const removeTooltip = (timeInt = 1500) => {
    setTimeout(()=> {
        switchTheme.blur()
    },timeInt)
}