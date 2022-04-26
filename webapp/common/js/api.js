const API_PATH = "/api"

async function getNumSockPuppets(ideology) {
    const req = await fetch(`${API_PATH}/getNumSockPuppets/${ideology}`);
    return await req.json();
}

async function getSockPuppet(ideology, puppetId) {
    const req = await fetch(`${API_PATH}/getSockPuppet/${ideology}/${puppetId}`);
    return await req.json();
}

async function getSockPuppetDates() {
    const req = await fetch(`${API_PATH}/getSockPuppetDates`);
    return await req.json();
}

async function getTopVideos(date) {
    const req = await fetch(`${API_PATH}/getTopVideos/${date}`);
    return await req.json();
}